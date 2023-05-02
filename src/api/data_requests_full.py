from src.utils import utils
import os
import requests
import pandas as pd
from functools import reduce

API_KEY = utils.read_api_key()
BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def make_request(endpoint, params=None):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(f'{BASE_URL}/{endpoint}', headers=headers, params=params)
    response.raise_for_status()
    return response.json()


# GAMES
# _________________________________________________________________
def get_games(year=None, week=None, team=None, seasonType=None):
    """
    Fetches college football games and results.

    Args:
        year (int, optional): The year of the season. Defaults to None.
        season (str, optional): The season to get games for (e.g. 'regular', 'postseason'). Defaults to None.
        team (str, optional): The abbreviation for the team to get games for (e.g. 'Michigan', 'UGA'). Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing game results.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('games', params=params)
    return pd.DataFrame(data)


def get_team_records(year=None, team=None, conference=None):
    """
    Fetches college football team records.

    Args:
        year (int, optional): The year of the season. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing team records.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('records', params=params)
    return pd.DataFrame(data)


def get_season_calendar(year):
    """
    Fetches the season calendar for college football.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing the season calendar.
    """
    data = make_request('calendar', params={'year': year})
    return pd.DataFrame(data)


def get_player_game_stats(year, week=None, seasonType=None, team=None):
    """
    Fetches player game stats.

    Args:
        year (int): The year of the season.
        season (str): The season of the year, e.g. 'regular' or 'postseason'.
        team (str): The team code of the team, e.g. 'Michigan' for Michigan.

    Returns:
        pd.DataFrame: A DataFrame containing player game stats.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('games/players', params=params)[0]
    data = [x for x in data['teams'] if x['school'] == team][0]['categories']

    def process_player_stats_category(data): 
        category_name = data['name']
        dfl = []
        for cat_subset in data['types']: 
            subset_name = cat_subset['name']
            category_rename_str = '{}_{}'.format(category_name, subset_name).lower()
            df = pd.DataFrame(cat_subset['athletes'])
            df = df.rename(columns = {'name': 'player_name', 'stat': category_rename_str})
            dfl.append(df) 
        dfc = reduce(lambda left, right: pd.merge(left, right, on=['id', 'player_name'], how='outer'), dfl)
        return dfc
    cat_dfl = [process_player_stats_category(x) for x in data]
    df = pd.concat(cat_dfl)
    return df
# get_player_game_stats(2022, team='Michigan', week=11)



def get_team_game_stats(year, team, seasonType=None, week=None):
    """
    Fetches team game stats.

    Args:
        year (int): The year of the season.
        season (str): The season of the year, e.g. 'regular' or 'postseason'.
        team (str): The team code of the team, e.g. 'Michigan' for Michigan.

    Returns:
        pd.DataFrame: A DataFrame containing team game stats.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    full_data = make_request('games/teams', params=params)
    data = [x for x in full_data[0]['teams'] if x['school'] == team][0]
    opponent_data = [x for x in full_data[0]['teams'] if x['school'] != team][0]
    opponent_name = opponent_data['school']
    opponent_conference = opponent_data['conference']
    opponent_points = opponent_data['points']
    opponent_homeAway = opponent_data['homeAway']
    opponent_stats = opponent_data['stats']
    opponent_data_dict = {item['category']: item['stat'] for item in opponent_stats}
    opponent_df = pd.DataFrame([opponent_data_dict])
    opponent_df['name'] = opponent_name
    opponent_df['conference'] = opponent_conference
    opponent_df['points'] = opponent_points
    opponent_df['homeAway'] = opponent_homeAway
    first_cols =  ['name', 'conference', 'points']
    opponent_df = opponent_df[first_cols + [x for x in opponent_df.columns if x not in first_cols]]
    opponent_df.columns = ['opponent_{}'.format(x) for x in opponent_df.columns]

    school = data['school']
    conference = data['conference']
    opponent = opponent_name
    points = data['points']
    homeAway = data['homeAway']
    stats = data['stats']
    data_dict = {item['category']: item['stat'] for item in stats}
    df = pd.DataFrame([data_dict])
    df['name'] = school
    df['opponent'] = opponent
    df['conference'] = conference
    df['points'] = points
    df['homeAway'] = homeAway
    df['week'] = week
    first_cols =  ['name', 'opponent', 'conference', 'points', 'homeAway', 'week']
    df = df[first_cols + [x for x in df.columns if x not in first_cols]]
    df = pd.concat([df, opponent_df], axis=1)
    return df

# get_team_game_stats(2019, week=1, team='Michigan')


# DRIVES
# _________________________________________________________________
def get_drives(year, seasonType=None, week=None, team=None, offense=None, defense=None, conference=None):
    """
    Fetches college football drive data and results.

    Args:
        year (int): The year of the season.
        season (str): The season of the year, e.g. 'regular' or 'postseason'.

    Returns:
        pd.DataFrame: A DataFrame containing drive data and results.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('drives', params=params)
    return pd.DataFrame(data)

# TEAMS
def get_team_season_stats(year, team, seasonType=None, week=None):
    """
    Fetches team statistics by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing team statistics by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/season', params)
    return pd.DataFrame(data)

# PLAYS
# _________________________________________________________________
def get_plays(year, seasonType: int = None, team: str = None, week: int = None):
    """
    Fetches college football play by play data for a specific season and team (optional).

    Args:
        season (int): The season year to fetch the data for.
        team (str, optional): The team abbreviation to fetch the data for.

    Returns:
        pd.DataFrame: A DataFrame containing play by play data.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('plays', params=params)
    return pd.DataFrame(data)


def get_play_stats(year, week=None, team=None):
    """
    Fetches college football play stats by play for a specific season and team (optional).

    Args:
        season (int): The season year to fetch the data for.
        team (str, optional): The team abbreviation to fetch the data for.

    Returns:
        pd.DataFrame: A DataFrame containing play stats by play.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('play/stats', params=params)
    return pd.DataFrame(data)


def get_play_stat_types():

    """
    Fetches types of player play stats.

    Returns:
        pd.DataFrame: A DataFrame containing types of player play stats.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('play/stats/types')
    return pd.DataFrame(data)



# TEAMS 
# _________________________________________________________________
def get_teams():
    """
    Fetches team information.

    Returns:
        pd.DataFrame: A DataFrame containing team information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('teams')
    return pd.DataFrame(data)


def get_fbs_teams(season):
    """
    Fetches the list of FBS teams.

    Args:
        season (str): The season to fetch FBS team information for. Format: YYYY

    Returns:
        pd.DataFrame: A DataFrame containing FBS team information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'teams/fbs/')
    return pd.DataFrame(data)


def get_team_rosters(team, year):
    """
    Fetches team rosters.

    Args:
        team (str): The team ID to fetch roster for.
        season (str): The season to fetch roster for. Format: YYYY

    Returns:
        pd.DataFrame: A DataFrame containing team rosters.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('roster', params=params)
    return pd.DataFrame(data)


def get_team_talent(team, season):
    """
    Fetches team talent composite rankings.

    Args:
        team (str): The team ID to fetch talent composite rankings for.
        season (str): The season to fetch talent composite rankings for. Format: YYYY

    Returns:
        pd.DataFrame: A DataFrame containing team talent composite rankings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('talent')
    return pd.DataFrame(data)


def get_team_matchup(team1, team2):
    """
    Fetches team matchup history.

    Args:
        team1 (str): The team ID of the first team.
        team2 (str): The team ID of the second team.

    Returns:
        pd.DataFrame: A DataFrame containing team matchup history.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'teams/matchup?team1={team1}&team2={team2}')
    return pd.DataFrame(data)


# COACHES 
# _________________________________________________________________

def get_coaches(year=None, team=None, firstName=None, lastName=None):
    """
    Fetches coaching records and history for a given year, season, and team.

    Args:
        year (int, optional): The year to retrieve coaching records for.
        season (str, optional): The season to retrieve coaching records for.
        team (str, optional): The team to retrieve coaching records for.

    Returns:
        pd.DataFrame: A DataFrame containing coaching records and history.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('coaches', params=params)
    return pd.DataFrame(data)


# PLAYERS 
# _________________________________________________________________

def search_player(query):
    """
    Searches for player information based on the query.

    Args:
        query (str): A search query for a player.

    Returns:
        pd.DataFrame: A DataFrame containing player information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('player/search', {'searchTerm': query})
    return pd.DataFrame(data)


def get_player_usage(year, team=None, position=None, playerId=None):
    """
    Fetches player usage metrics broken down by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing player usage metrics.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('player/usage', params=params)
    df = pd.DataFrame(data)
    usage_df = df['usage'].apply(lambda x: pd.Series(x)).add_prefix('usage_')
    result_df = pd.concat([df.drop(columns=['usage']), usage_df], axis=1)
    return result_df


def get_team_returning_production(year, team=None):
    """
    Fetches team returning production metrics for a given year and team.

    Args:
        year (int): The year of the season.
        team (str, optional): The team to retrieve returning production metrics for.

    Returns:
        pd.DataFrame: A DataFrame containing team returning production metrics.
    """
    params = {'year': year}
    if team is not None:
        params['team'] = team
    data = make_request('player/returning', params=params)
    return pd.DataFrame(data)


def get_player_stats_by_season(year, team=None):
    """
    Fetches player stats by season for a given year and team.

    Args:
        year (int): The year of the season.
        team (str, optional): The team to retrieve player stats for.

    Returns:
        pd.DataFrame: A DataFrame containing player stats by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('stats/player/season', params=params)
    return pd.DataFrame(data)


def get_transfer_portal_by_season(year, team=None):
    """
    Fetches transfer portal information by season for a given year and team.

    Args:
        year (int): The year of the season.
        team (str, optional): The team to retrieve transfer portal information for.

    Returns:
        pd.DataFrame: A DataFrame containing transfer portal information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('player/portal', params=params)
    return pd.DataFrame(data)




# STATS
#_________________________________________________________________________

def get_team_season_stats(year=None, team=None, conference=None):
    """
    Fetches team statistics by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing team statistics by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/season/', params=params)
    return pd.DataFrame(data)


def get_advanced_season_stats(year=None, team=None, conference=None):
    """
    Fetches advanced team metrics by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing advanced team metrics by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/season/advanced/', params=params)
    return pd.DataFrame(data)


def get_advanced_game_stats(year, week, team=None, opponent=None):
    """
    Fetches advanced team metrics by game.

    Args:
        year (int): The year of the season.
        week (int): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing advanced team metrics by game.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/game/advanced/', params=params)
    return pd.DataFrame(data)


def get_team_stat_categories():
    """
    Fetches team stat categories.

    Returns:
        pd.DataFrame: A DataFrame containing team stat categories.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('stats/categories')
    return pd.DataFrame(data)

