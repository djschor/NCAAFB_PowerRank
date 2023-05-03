import pandas as pd 
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
# import utils as utils located as src/utils/utils.py
from backend.src.utils import utils, gcp_utils as gutils
from backend.src.api import data_requests as dr
from backend.src.processing import calculate_qb_metrics as cqm, calculate_defense_metrics as cdm

def get_defense_game_metrics(team, week, year):
    try:
        plays = dr.get_plays(year=year, team=team, week=week)
        defense_plays = plays[plays.defense==team]

        pcpa = cdm.pass_completion_percentage_allowed(defense_plays)
        dsr = cdm.defensive_sack_rate(defense_plays)
        ir = cdm.interception_rate(defense_plays)
        dpr = cdm.defensive_passer_rating(defense_plays)
        oppsr = cdm.opponents_passing_play_success_rate(defense_plays)
        df = pd.DataFrame([[team, week, year, pcpa, dsr, ir, dpr, oppsr]], columns=['team', 'week', 'year', 'pass_completion_percentage_allowed', 'defensive_sack_rate', 'interception_rate', 'defensive_passer_rating', 'opponents_passing_play_success_rate'])
        return df
    except Exception as e:
        print(e)
    

def get_defense_game_metrics_all_games(team, year):
    games = dr.get_games(year=year, team=team)
    df = pd.concat([get_defense_game_metrics(team, week, year) for week in games.week.tolist()])
    return df

def calculate_relative_defensive_metrics(defense_df): 
    low_score_list = ['pass_completion_percentage_allowed']
    score_cols = [ 'pass_completion_percentage_allowed', 'defensive_sack_rate', 'interception_rate', 'defensive_passer_rating', 'opponents_passing_play_success_rate']

    # define base ranking function 
    def get_ranks_and_pcts(df, score_columns, low_score_list=None): 
        for qcol in score_columns:
            if qcol in low_score_list:
                df['{}_relative_score'.format(qcol)] = 100 - MinMaxScaler(feature_range=(0, 40)).fit_transform(df[qcol].values.reshape(-1, 1)).reshape(-1)
            else:
                df['{}_relative_score'.format(qcol)] = MinMaxScaler(feature_range=(60, 100)).fit_transform(df[qcol].values.reshape(-1, 1)).reshape(-1)
            df['{}_relative_rank'.format(qcol)] = df['{}_relative_score'.format(qcol)].rank(method='max', ascending=False)
        return df 
    # if scoring columns, calculate percentiles and ranks
    df = get_ranks_and_pcts(defense_df, score_cols, low_score_list)
    return df


def calculate_week_competitive_metrics(df, week):
    low_score_list = ['pass_completion_percentage_allowed']
    score_cols = [ 'pass_completion_percentage_allowed', 'defensive_sack_rate', 'interception_rate', 'defensive_passer_rating', 'opponents_passing_play_success_rate']

    competitive_metrics_df = df[df['week'] == week].copy()

    for qcol in score_cols:
        competitive_metrics_df[f"{qcol}_competitive_rank"] = competitive_metrics_df[qcol].rank(method='max', ascending=False)
        if qcol in low_score_list:
            competitive_metrics_df['{}_competitive_score'.format(qcol)] = 100 - MinMaxScaler(feature_range=(0, 40)).fit_transform(competitive_metrics_df[qcol].values.reshape(-1, 1)).reshape(-1)
        else:
            competitive_metrics_df['{}_competitive_score'.format(qcol)] = MinMaxScaler(feature_range=(60, 100)).fit_transform(competitive_metrics_df[qcol].values.reshape(-1, 1)).reshape(-1)
        competitive_metrics_df['{}_competitive_rank'.format(qcol)] = competitive_metrics_df['{}_competitive_score'.format(qcol)].rank(method='max', ascending=False)
    return competitive_metrics_df


def score_defense_total(df):
    relative_cols = [col for col in df.columns if col.endswith('_relative_score')]
    competitive_cols = [col for col in df.columns if col.endswith('_competitive_score')]
    
    # Calculate relative and competitive scores separately
    df['relative_score'] = df[relative_cols].mean(axis=1)
    df['competitive_score'] = df[competitive_cols].mean(axis=1)
    
    # Calculate weighted average of relative and competitive scores
    df['defense_total_score'] = 0.9 * df['competitive_score'] + 0.1 * df['relative_score']
    df['defense_total_score'] = MinMaxScaler(feature_range=(40, 100)).fit_transform(df['defense_total_score'].values.reshape(-1, 1)).reshape(-1)
    df['defense_total_rank'] = df['defense_total_score'].rank(method='max', ascending=False)

    df = df.drop(columns=relative_cols+competitive_cols)
    return df


def calculate_power_5_defense_metrics_save_gcp(year):
    print(f"Calculating defensive metrics for Power 5 teams in {year}...")
    # Get all Power 5 teams
    power5_teams = dr.get_fbs_teams(season=year)
    team_ids = power5_teams['id'].tolist()
    team_names = power5_teams['school'].tolist()

    # Calculate defensive metrics for each team and save to a DataFrame
    all_defense_metrics = []

    for team_name in team_names:
        defense_metrics = get_defense_game_metrics_all_games(team_name, year)
        relative_defense_metrics = calculate_relative_defensive_metrics(defense_metrics)
        all_defense_metrics.append(relative_defense_metrics)

    all_defense_metrics_df = pd.concat(all_defense_metrics)

    # Get the list of unique weeks in the DataFrame
    unique_weeks = all_defense_metrics_df['week'].unique()

    # Calculate competitive metrics for each week
    competitive_defense_metrics = []
    for week in unique_weeks:
        week_competitive_metrics = calculate_week_competitive_metrics(all_defense_metrics_df, week)
        competitive_defense_metrics.append(week_competitive_metrics)

    competitive_defense_metrics_df = pd.concat(competitive_defense_metrics)

    # Calculate the total defense score
    scored_defense_df = score_defense_total(competitive_defense_metrics_df)

    scored_defense_df['pk'] = scored_defense_df['team'] + '_' + scored_defense_df['week'].astype(str) + '_' + scored_defense_df['year'].astype(str)
    # Save the data to a GCP collection called "defense"
    print("Saving defensive metrics to GCP...")
    gutils.batch_save_data_firestore(scored_defense_df, "defense", 'pk')

    print("Saved defensive metrics to GCP.")
