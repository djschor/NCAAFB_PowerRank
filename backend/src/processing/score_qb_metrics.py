import pandas as pd 
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
# import utils as utils located as src/utils/utils.py
from backend.src.utils import utils, gcp_utils as gutils
from backend.src.api import data_requests as dr
from backend.src.processing import calculate_qb_metrics as cqm, calculate_defense_metrics as cdm, score_defense_metrics as sdm, score_qb_metrics as sqm
import numpy as np 
from functools import reduce
import time 
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
from fuzzywuzzy import fuzz, process

from retry import retry
import os


def read_plays_csv(team, week):
    file_path = os.environ.get('LOCAL_PLAYS_PATH')
    file_name = f"{team}_{week}.csv"
    full_path = os.path.join(file_path, file_name)
    cols=['id', 'offense', 'offense_conference', 'defense', 'defense_conference',
       'home', 'away', 'offense_score', 'defense_score', 'game_id', 'drive_id',
       'drive_number', 'play_number', 'period', 'clock', 'offense_timeouts',
       'defense_timeouts', 'yard_line', 'yards_to_goal', 'down', 'distance',
       'scoring', 'yards_gained', 'play_type', 'play_text', 'ppa', 'wallclock',
       'week', 'team', 'year']
    empty_df = pd.DataFrame(columns=cols) 
    
    try:
        plays_df = pd.read_csv(full_path)
        return plays_df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return empty_df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return empty_df

def get_qb_game_metrics(player, team, week, year): 
    print(player, week, year)
    try:
        plays = read_plays_csv(team=team, week=week)#.drop(columns=['Unnamed: 0'])
        if 'play_text' in plays.columns:
            player_plays = plays[plays.play_text.str.contains(player, na=False)]
            player_plays = player_plays[player_plays.offense==team]

            if player_plays.empty:
                # Return a DataFrame with null values
                print('No plays for {} in week {} of {}'.format(player, week, year))
                return pd.DataFrame([[player, team, week, year, None, None, None, None, None, None, None, None, None]], columns=['player', 'team', 'week', 'year', 'aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score'])

            # Get the opponent team
            opponent_team = player_plays.iloc[0]['defense']

            # Get the average defense_total_score of the opponent for weeks before the current week
            average_defense_score = get_opponent_defense_metrics(opponent_team, week, year)


            aqs = cqm.adaptive_quarterback_score(player_plays)
            qpi = cqm.quarterback_passing_index(player_plays)
            sei = cqm.scramble_efficiency_index(player_plays)
            crae = cqm.completion_rate_above_expected(player_plays)
            dmi = cqm.decision_making_index(player_plays)
            ppi = cqm.pressure_performance_index(player_plays)
            adpsr = cqm.adjusted_deep_pass_success_rate(player_plays)
            reer = cqm.red_zone_efficiency_rating(player_plays)
            df = pd.DataFrame([[player, team, week, year, aqs, qpi, sei, crae, dmi, ppi, adpsr, reer, average_defense_score]], columns=['player', 'team', 'week', 'year', 'aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score'])
        else:
            df = pd.DataFrame([[player, team, week, year, None, None, None, None, None, None, None, None, None]], columns=['player', 'team', 'week', 'year', 'aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score'])
    except ValueError as e: 
        print('Error in QB Game Metrics: ', e)
        df = pd.DataFrame([[player, team, week, year, None, None, None, None, None, None, None, None, None]], columns=['player', 'team', 'week', 'year', 'aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score'])
    return df 
# _____     
def get_qb_game_metrics_all_games(player, team, year):
    games = dr.get_games(year=year, team=team)
    df = pd.concat([get_qb_game_metrics(player, team, week, year) for week in games.week.tolist()])
    return df 

def get_opponent_defense_metrics(opponent_team, week, year):
    base_path = os.environ.get('LOCAL_DEFENSE_PATH')
    
    # Get all the files matching the given team, week, and year
    files = [f for f in os.listdir(base_path) if f.startswith(f"{opponent_team}_{week}_{year}") and f.endswith('.csv')]

    # Use a generator to calculate the sum and length of defense_scores simultaneously
    sum_defense_scores, n = (0, 0)
    for file in files:
        data = pd.read_csv(os.path.join(base_path, file))
        defense_total_score = data['defense_total_score'].iloc[0]
        sum_defense_scores += defense_total_score
        n += 1

    # Calculate the average defense_total_score for weeks before the current week
    average_defense_score = sum_defense_scores / n if n > 0 else None

    return average_defense_score


def get_ranks_and_pcts(df, score_columns, low_score_list=None):
    df = df.copy()
    for qcol in score_columns:
        if qcol in low_score_list:
            df.loc[:, '{}_relative_score'.format(qcol)] = 100 - MinMaxScaler(feature_range=(0, 40)).fit_transform(df[qcol].values.reshape(-1, 1)).reshape(-1)
        else:
            df.loc[:, '{}_relative_score'.format(qcol)] = MinMaxScaler(feature_range=(60, 100)).fit_transform(df[qcol].values.reshape(-1, 1)).reshape(-1)
        df.loc[:, '{}_relative_rank'.format(qcol)] = df['{}_relative_score'.format(qcol)].rank(method='max', ascending=False)
    return df


def calculate_qb_relative_metrics(qb_df):
    qb_df =  qb_df.copy()
    score_cols = ['aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score']
    low_score_list = []  # Add any metrics where a lower score is better, if applicable

    # Replace infinite values with np.nan
    qb_df = qb_df.replace([np.inf, -np.inf], np.nan)

    # Handle missing values as needed (e.g., drop rows with missing values, fill with mean or median, etc.)
    # For example, to drop rows with any missing values in the score columns:
    qb_df = qb_df.dropna(subset=score_cols)

    all_qb_relative_metrics = []
    for player in qb_df['player'].unique():
        player_df = qb_df[qb_df['player'] == player]
        # Calculate percentiles and ranks for the QB performance metrics
        player_relative_metrics = get_ranks_and_pcts(player_df, score_cols, low_score_list)
        all_qb_relative_metrics.append(player_relative_metrics)

    return pd.concat(all_qb_relative_metrics)


def calculate_qb_week_competitive_metrics(df, week):
    df = df.copy()
    score_cols = ['aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score']
    low_score_list = []  # Add any metrics where a lower score is better, if applicable

    competitive_metrics_df = df[df['week'] == week].copy()

    for qcol in score_cols:
        if qcol in low_score_list:
            competitive_metrics_df['{}_competitive_score'.format(qcol)] = 100 - MinMaxScaler(feature_range=(0, 40)).fit_transform(competitive_metrics_df[qcol].values.reshape(-1, 1)).reshape(-1)
        else:
            competitive_metrics_df['{}_competitive_score'.format(qcol)] = MinMaxScaler(feature_range=(60, 100)).fit_transform(competitive_metrics_df[qcol].values.reshape(-1, 1)).reshape(-1)
        competitive_metrics_df['{}_competitive_rank'.format(qcol)] = competitive_metrics_df['{}_competitive_score'.format(qcol)].rank(method='max', ascending=False)
    return competitive_metrics_df


def score_qb_total(df):
    df = df.copy()
    relative_cols = [col for col in df.columns if col.endswith('_relative_score')]
    competitive_cols = [col for col in df.columns if col.endswith('_competitive_score')]
    score_cols = ['aqs', 'qpi', 'sei', 'crae', 'dmi', 'ppi', 'adpsr', 'reer', 'defense_score']

    # Calculate relative and competitive scores separately
    df.loc[:, 'qb_relative_score'] = df[relative_cols].mean(axis=1)
    df.loc[:, 'qb_competitive_score'] = df[competitive_cols].mean(axis=1)
    
    # Calculate weighted average of relative and competitive scores
    df.loc[:, 'qb_total_score'] = 0.9 * df['qb_competitive_score'] + 0.1 * df['qb_relative_score']
    df.loc[:, 'qb_total_score'] = MinMaxScaler(feature_range=(60, 100)).fit_transform(df['qb_total_score'].values.reshape(-1, 1)).reshape(-1)
    df.loc[:, 'qb_total_rank'] = df['qb_total_score'].rank(method='max', ascending=False)
    # df = df.drop(columns=relative_cols+competitive_cols)
    return df

def get_game_data(df, year):
    output_df = pd.DataFrame(columns=['week', 'conference', 'conference_game', 'opponent_name', 'is_home_game', 'win', 'points', 'point_differential', 'excitement_index', 'post_win_prob', 'post_win_differential', 'pregame_elo', 'pregame_elo_differential', 'postgame_elo'])

    for index, row in df.drop_duplicates(subset=['week', 'team']).iterrows():
        week = row['week']
        team = row['team']

        game_data = dr.get_games(year, week, team)

        is_home_game = (game_data['home_team'] == team).iloc[0]

        conference = game_data['home_conference' if is_home_game else 'away_conference'].iloc[0]
        conference_game = int(game_data['home_conference'].iloc[0] == game_data['away_conference'].iloc[0])
        opponent_name = game_data['away_team' if is_home_game else 'home_team'].iloc[0]
        win = int(game_data['home_points'].iloc[0] > game_data['away_points'].iloc[0]) if is_home_game else int(game_data['away_points'].iloc[0] > game_data['home_points'].iloc[0])
        points = game_data['home_points' if is_home_game else 'away_points'].iloc[0]
        point_differential = points - game_data['away_points' if is_home_game else 'home_points'].iloc[0]
        excitement_index = game_data['excitement_index'].iloc[0]
        post_win_prob = game_data['home_post_win_prob' if is_home_game else 'away_post_win_prob'].iloc[0]
        post_win_differential = post_win_prob - game_data['away_post_win_prob' if is_home_game else 'home_post_win_prob'].iloc[0]
        pregame_elo = game_data['home_pregame_elo' if is_home_game else 'away_pregame_elo'].iloc[0]
        pregame_elo_differential = pregame_elo - game_data['away_pregame_elo' if is_home_game else 'home_pregame_elo'].iloc[0]
        postgame_elo = game_data['home_postgame_elo' if is_home_game else 'away_postgame_elo'].iloc[0]

        output_df = output_df.append({
            'week': week,
            'conference': conference,
            'conference_game': conference_game,
            'opponent_name': opponent_name,
            'is_home_game': int(is_home_game),
            'win': win,
            'points': points,
            'point_differential': point_differential,
            'excitement_index': excitement_index,
            'post_win_prob': post_win_prob,
            'post_win_differential': post_win_differential,
            'pregame_elo': pregame_elo,
            'pregame_elo_differential': pregame_elo_differential,
            'postgame_elo': postgame_elo}, ignore_index=True)

    merged_df = df.merge(output_df, how='left', on=['week', 'team'])
    return merged_df


def calculate_qb_performance_weekly_metrics_save_gcp(year, saved=True):
    print(f"Calculating QB performance metrics for {year}...")

    # Get all FBS teams
    fbs_teams = dr.get_fbs_teams(season=year)
    team_names = fbs_teams['school'].tolist()
    # team_names = ['Michigan']

    def process_team_qb_data(team_name):
        print(f"Processing {team_name} QB data...")
        # Fetch team rosters and find the quarterbacks
        team_roster = dr.read_team_roster_csv(team_name, year)
        qb_roster = team_roster[team_roster['position'] == 'QB']
        if not qb_roster.empty:
            # Get player usage data for the QBs
            qb_usages = dr.read_qb_usage_csv(team_name)
            starting_qbs = qb_usages[qb_usages['id'].isin(qb_roster['id'])].sort_values(by='usage_overall', ascending=False).head(2)

            # Determine the starting quarterback(s)
            if starting_qbs.empty:
                # No dominant starter, get first and second string QBs by usage
                starting_qbs = qb_usages.nlargest(1, 'usage_overall')
            qb_data = []
            for _, starting_qb in starting_qbs.iterrows():
                if starting_qb['name'] is not None and starting_qb['team'] is not None:
                    qb_name = starting_qb['name']
                    qb_team = starting_qb['team']
                    qb_df = get_qb_game_metrics_all_games(qb_name, qb_team, year).fillna(0)
                    qb_df.to_csv(os.environ.get('LOCAL_QB_PERFORMANCE_PATH') + qb_name + '.csv')
                    qb_data.append(qb_df)
            print(f"Completed {team_name} QB data")
            return pd.concat(qb_data, ignore_index=True) if qb_data else None
        else:
            return pd.DataFrame()

    # get the qb weekly data for each qquarterback, if not saved calculate manually, if saved then read the local csvs
    if saved==False: 
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_team_qb_data, team_name) for team_name in team_names]
            results = [future.result() for future in as_completed(futures)]
        all_qb_data_df = pd.concat(results)
            # save player names to meta collection gcp 
        qb_names = all_qb_data_df['player'].unique().tolist()
        gutils.save_data_to_firestore_id({'qbs': qb_names}, gutils.get_firestore_client_db(), 'meta', 'qbs')
    else:
        def read_csv(file_path):
            return pd.read_csv(file_path)

        def concatenate_qb_weekly_saved_csvs():
            folder_path = os.environ.get('LOCAL_QB_PERFORMANCE_PATH')
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            with ThreadPoolExecutor() as executor:
                dataframes = list(executor.map(read_csv, [os.path.join(folder_path, f) for f in csv_files]))
            concatenated_dataframe = pd.concat(dataframes, ignore_index=True)
            return concatenated_dataframe
        all_qb_data_df = concatenate_qb_weekly_saved_csvs()

    # Calculate relative metrics for each QB
    relative_qb_metrics = calculate_qb_relative_metrics(all_qb_data_df)

    # Get the list of unique weeks in the DataFrame
    unique_weeks = relative_qb_metrics['week'].unique()

    # Execute calculate_qb_week_competitive_metrics concurrently using a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        week_competitive_metrics_futures = [executor.submit(functools.partial(calculate_qb_week_competitive_metrics, relative_qb_metrics), week) for week in unique_weeks]

        week_competitive_metrics = []
        for future in as_completed(week_competitive_metrics_futures):
            week_competitive_metrics.append(future.result())

    competitive_qb_metrics_df = pd.concat(week_competitive_metrics)

    # Calculate the total defense score
    qb_score_df = score_qb_total(competitive_qb_metrics_df)

    # Get the game data for each team/week in qb df
    qb_df = get_game_data(qb_score_df, year)
    # Save the data to a GCP collection called "qb_performance"
    print("Saving QB performance metrics to GCP...")
    qb_df['pk'] = qb_df['player'] + '_' + qb_df['week'].astype(str) + '_' + qb_df['year'].astype(str)    
    gutils.batch_save_data_firestore(qb_df, "qb", 'pk')

    print("Saved QB performance metrics to GCP.")
    return 

def calculate_save_overall_qb_rankings(qb_df=None, year=2022):
    if qb_df==None:
        qb_df = pd.DataFrame(gutils.scan_firestore_collection('qb'))
    qbs = qb_df.player.unique().tolist()
    overall_qb_rankings = []
    metric_cols = ['adpsr', 'aqs', 'crae', 'defense_score', 'dmi', 'ppi', 'qpi', 'reer', 'sei', 'qb_competitive_score', 'qb_relative_score', 'qb_total_score' ]
    
    for qb in qbs:
        print(f"Calculating avg QB rankings for {qb}...")

        qb_performance_data = qb_df[qb_df.player == qb].copy()
        if not qb_performance_data.empty:
            # Extract numeric columns
            numeric_columns = qb_performance_data.select_dtypes(include=['number']).columns

            # Calculate the average for each numeric column
            avg_qb_data = {}
            for column in metric_cols:
                avg_qb_data[f'avg_{column}'] = qb_performance_data[column].mean()

            # Append player and year to the result
            avg_qb_data['player'] = qb
            avg_qb_data['year'] = year

            overall_qb_rankings.append(avg_qb_data)

    # Convert the list of dictionaries to a DataFrame
    overall_qb_rankings_df = pd.DataFrame(overall_qb_rankings)

    # Calculate the rankings based on the average QB total score and competitive score
    for metric in metric_cols:
        overall_qb_rankings_df[f'{metric}_rank'] = overall_qb_rankings_df[f'avg_{metric}'].rank(ascending=False)
        overall_qb_rankings_df[f'{metric}_score'] = MinMaxScaler(feature_range=(60, 100)).fit_transform(overall_qb_rankings_df[f'avg_{metric}'].values.reshape(-1, 1)).reshape(-1)
    overall_qb_rankings_df = overall_qb_rankings_df.rename(columns={x:"_".join(x.split('_')[:-1]) for x in overall_qb_rankings_df.columns if 'score_score' in x})

    # Save the overall QB rankings to Firestore
    gutils.batch_save_data_firestore(overall_qb_rankings_df, f"qb_overall_rankings_{year}", id='player')
    print(f"Saved overall QB rankings for {year} to Firestore.")
    return
