import os
from dotenv import load_dotenv
import pandas as pd
def get_base_path():
    """
    Gets the base path of the project located at the base NCAAFB_POWER_RANK directory, two parents above the current path. 

    Returns:
        str: The base path of the project.
    """
    current_path = os.path.abspath(__file__)
    parent_path = os.path.dirname(current_path)
    grandparent_path = os.path.dirname(parent_path)
    base_path = os.path.dirname(grandparent_path)
    return base_path

def read_api_key():
    """
    Reads the CFB_API_KEY from the .env file.

    Returns:
        str: The CFB_API_KEY.
    """
    # Load the environment variables from the .env file
    # base_path = get_base_path()
    # dotenv_path = os.path.join(base_path, '.env')
    # load_dotenv(dotenv_path)

    # # Read the CFB_API_KEY from the environment variables
    # api_key = os.getenv('CFB_API_KEY')
    api_key = 'wqBg+0bIHmq2BtxbbG5Nl3OBs33jK7MDCVFNIlomT6vC/u0udTA1PF+KcStlGUSM'
    return api_key


def read_2022_game_csvs():
    directory = "/Users/djschor/Projects/ncaafb_power_rank/data/games_2022/"
    # initialize an empty DataFrame to store all CSV data
    all_data = pd.DataFrame()

    # loop over all CSV files in the directory and append them to the DataFrame
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            data = pd.read_csv(file_path)
            all_data = pd.concat([all_data, data], ignore_index=True)

    return all_data

def read_2022_roster_csvs():
    directory = "/Users/djschor/Projects/ncaafb_power_rank/data/rosters_2022/"
    # initialize an empty DataFrame to store all CSV data
    all_data = pd.DataFrame()

    # loop over all CSV files in the directory and append them to the DataFrame
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            data = pd.read_csv(file_path)
            all_data = pd.concat([all_data, data], ignore_index=True)

    return all_data


def read_2022_game_csvs():
    directory = "/Users/djschor/Projects/ncaafb_power_rank/data/games_2022/"
    # initialize an empty DataFrame to store all CSV data
    all_data = pd.DataFrame()

    # loop over all CSV files in the directory and append them to the DataFrame
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            data = pd.read_csv(file_path)
            all_data = pd.concat([all_data, data], ignore_index=True)

    return all_data



def add_team_column_and_save(directory):
    # loop over all CSV files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)

            # read CSV file into a DataFrame
            data = pd.read_csv(file_path)

            # extract the team name from the file name and add it as a new column
            team_name = file_name.split("_")[0]
            data['team'] = team_name

            # save the modified DataFrame back to the same file
            data.to_csv(file_path, index=False)

# directory = "/Users/djschor/Projects/ncaafb_power_rank/data/games_2022/"
# add_team_column_and_save(directory)


import time

def process_save_game_data(year, week, team):
    print("Processing", team, "in week", week)
    save_dir = '/Users/djschor/Projects/ncaafb_power_rank/data/games_2022'
    file_path = os.path.join(save_dir, f"{team}_{week}.csv")
    if os.path.isfile(file_path):
        return pd.read_csv(file_path).to_dict(orient='records')[0]
    try:
        game_data = dr.get_games(year, week, team)
    except:
        print("Error retrieving game data for", team, "in week", week)
        return pd.DataFrame({'week': [],
        'conference': [],
        'conference_game': [],
        'opponent_name': [],
        'is_home_game': [],
        'win': [],
        'points': [],
        'point_differential': [],
        'excitement_index': [],
        'post_win_prob': [],
        'post_win_differential': [],
        'pregame_elo': [],
        'pregame_elo_differential': [],
        'postgame_elo': []})



    try: 
        is_home_game = (game_data['home_team'] == team).iloc[0]
        conference = game_data['home_conference' if is_home_game else 'away_conference'].iloc[0]
        conference_game = int(game_data['home_conference'].iloc[0] == game_data['away_conference'].iloc[0])
        opponent_name = game_data['away_team' if is_home_game else 'home_team'].iloc[0]
        win = int(game_data['home_points'].iloc[0] > game_data['away_points'].iloc[0]) if is_home_game else int(game_data['away_points'].iloc[0] > game_data['home_points'].iloc[0])
        points = game_data['home_points' if is_home_game else 'away_points'].iloc[0]
        point_differential = points - game_data['away_points' if is_home_game else 'home_points'].iloc[0]
        excitement_index = game_data['excitement_index'].iloc[0]
        post_win_prob = pd.to_numeric(game_data['home_post_win_prob' if is_home_game else 'away_post_win_prob'].iloc[0])
        away_post_win_prob = pd.to_numeric(game_data['away_post_win_prob' if is_home_game else 'home_post_win_prob'].iloc[0])
        post_win_differential = post_win_prob - away_post_win_prob
        pregame_elo = pd.to_numeric(game_data['home_pregame_elo' if is_home_game else 'away_pregame_elo'].iloc[0])
        away_pregame_elo = pd.to_numeric(game_data['away_pregame_elo' if is_home_game else 'home_pregame_elo'].iloc[0])
        pregame_elo_differential = pregame_elo - away_pregame_elo
        postgame_elo = pd.to_numeric(game_data['home_postgame_elo' if is_home_game else 'away_postgame_elo'].iloc[0])

        data = {'week': week,
                'team': team,
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
                'postgame_elo': postgame_elo}
    except Exception as e:
        print(e)
        print("Error processing game data for", team, "in week", week)
        return pd.DataFrame({'week': [],
        'conference': [],
        'conference_game': [],
        'opponent_name': [],
        'is_home_game': [],
        'win': [],
        'points': [],
        'point_differential': [],
        'excitement_index': [],
        'post_win_prob': [],
        'post_win_differential': [],
        'pregame_elo': [],
        'pregame_elo_differential': [],
        'postgame_elo': []})
    
    try:
        df = pd.DataFrame(data, index=[0])
        df.to_csv(file_path, index=False)
        print("Saved game data for", team, "in week", week)
        return df
    except:
        print("Error saving game data for", team, "in week", week)
        time.sleep(30) # wait for 1 second to prevent overrunning the API
    
    
import concurrent.futures

def save_local_game_data(df):
    output_list = []
    unique_weeks_teams = df.drop_duplicates(subset=['week', 'team'])[['week', 'team']].values.tolist()
    for week, team in unique_weeks_teams:
        output_list.append(process_save_game_data(year, week, team))    
    output_df = pd.DataFrame(output_list, columns=['week', 'team', 'conference', 'conference_game', 'opponent_name', 'is_home_game', 'win', 'points', 'point_differential', 'excitement_index', 'post_win_prob', 'post_win_differential', 'pregame_elo', 'pregame_elo_differential', 'postgame_elo'])
    merged_df = df.merge(output_df, how='left', on=['week', 'team'])
    return merged_df


def add_team_column_and_save_with_roster(directory, roster_df):
    # loop over all CSV files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)

            # read CSV file into a DataFrame
            data = pd.read_csv(file_path).drop(columns=['team'])

            # merge with roster DataFrame to add team column
            data = pd.merge(data, roster_df[['player', 'team']], on='player', how='left')

            # drop all columns except 'team' from the roster DataFrame
            data = data[['team']]

            # save the modified DataFrame back to the same file
            data.to_csv(file_path, index=False)

# directory = "/Users/djschor/Projects/ncaafb_power_rank/data/qb_performance_2022"
# roster_df = read_2022_roster_csvs()
# roster_df['player'] = roster_df.first_name + ' ' + roster_df.last_name
# add_team_column_and_save_with_roster(directory, roster_df)
