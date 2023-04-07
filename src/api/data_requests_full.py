from src.utils import utils
import os
import requests
import pandas as pd
API_KEY = utils.read_api_key()

BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def make_request(endpoint, params=None):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(f'{BASE_URL}/{endpoint}', headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_conferences():
    """
    Fetches a list of college football conferences.

    Returns:
        pd.DataFrame: A DataFrame containing conferences information.
    """
    data = make_request('conferences')
    return pd.DataFrame(data)

def get_venues():
    """
    Fetches a list of college football venues.

    Returns:
        pd.DataFrame: A DataFrame containing venue information.
    """
    data = make_request('venues')
    return pd.DataFrame(data)

def get_coaches():
    """
    Fetches a list of college football coaches with their records and history.

    Returns:
        pd.DataFrame: A DataFrame containing coaching records and history.
    """
    data = make_request('coaches')
    return pd.DataFrame(data)

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
    data = make_request('games', params=params)
    return pd.DataFrame(data)


def get_team_game_stats(year, season, team, week=None):
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
    data = make_request(f'{year}/{season}/games/teams/{team}')
    return pd.DataFrame(data)


# DRIVES
# _________________________________________________________________
def get_drives(year, season):
    """
    Fetches college football drive data and results.

    Args:
        year (int): The year of the season.
        season (str): The season of the year, e.g. 'regular' or 'postseason'.

    Returns:
        pd.DataFrame: A DataFrame containing drive data and results.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'{year}/{season}/drives')
    return pd.DataFrame(data)

# PLAYS
# _________________________________________________________________
def get_plays(seasonType: int = None, team: str = None, week: int = None):
    """
    Fetches college football play by play data for a specific season and team (optional).

    Args:
        season (int): The season year to fetch the data for.
        team (str, optional): The team abbreviation to fetch the data for.

    Returns:
        pd.DataFrame: A DataFrame containing play by play data.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('coaches', params=params)
    return pd.DataFrame(data)


def get_play_types():
    """
    Fetches college football play types.

    Returns:
        pd.DataFrame: A DataFrame containing play types.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('plays/types')
    return pd.DataFrame(data)


def get_play_stats(season: int, team: str = None):
    """
    Fetches college football play stats by play for a specific season and team (optional).

    Args:
        season (int): The season year to fetch the data for.
        team (str, optional): The team abbreviation to fetch the data for.

    Returns:
        pd.DataFrame: A DataFrame containing play stats by play.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    if team:
        data = make_request(f'season/{season}/team/{team}/stats/plays')
    else:
        data = make_request(f'season/{season}/stats/plays')
    return pd.DataFrame(data)


def get_play_stat_types():

    """
    Fetches types of player play stats.

    Returns:
        pd.DataFrame: A DataFrame containing types of player play stats.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('plays/stats/types')
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
    data = make_request(f'teams/fbs/{season}')
    return pd.DataFrame(data)


def get_team_rosters(team, season):
    """
    Fetches team rosters.

    Args:
        team (str): The team ID to fetch roster for.
        season (str): The season to fetch roster for. Format: YYYY

    Returns:
        pd.DataFrame: A DataFrame containing team rosters.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'team/{team}/{season}/roster')
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
    data = make_request(f'team/{team}/{season}/talent')
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

# CONFERENCE 
# _________________________________________________________________

def get_conferences(year=None, season=None):
    """
    Fetches conference information for a given year and season.

    Args:
        year (int, optional): The year to retrieve conference information for.
        season (str, optional): The season to retrieve conference information for.

    Returns:
        pd.DataFrame: A DataFrame containing conference information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('conferences', params=params)
    return pd.DataFrame(data)
 
 # VENUES
 # _________________________________________________________________

def get_venues(year=None, season=None, team=None):
    """
    Fetches arena and venue information for a given year, season, and team.

    Args:
        year (int, optional): The year to retrieve venue information for.
        season (str, optional): The season to retrieve venue information for.
        team (str, optional): The team to retrieve venue information for.

    Returns:
        pd.DataFrame: A DataFrame containing arena and venue information.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('venues', params=params)
    return pd.DataFrame(data)


# COACHES 
# _________________________________________________________________

def get_coaches(year=None, season=None, team=None):
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
    data = make_request('player/search', {'search': query})
    return pd.DataFrame(data)


def get_player_usage(year):
    """
    Fetches player usage metrics broken down by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing player usage metrics.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('player/usage', {'year': year})
    return pd.DataFrame(data)


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

def get_team_season_stats(year):
    """
    Fetches team statistics by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing team statistics by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/season/{year}')
    return pd.DataFrame(data)


def get_advanced_season_stats(year):
    """
    Fetches advanced team metrics by season.

    Args:
        year (int): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing advanced team metrics by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/season/advanced/{year}')
    return pd.DataFrame(data)


def get_advanced_game_stats(year, week):
    """
    Fetches advanced team metrics by game.

    Args:
        year (int): The year of the season.
        week (int): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing advanced team metrics by game.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'stats/game/advanced/{year}/{week}')
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


# DRAFT
#_________________________________________________________________________
def get_nfl_teams():
    """
    Fetches a list of NFL teams.

    Returns:
        pd.DataFrame: A DataFrame containing a list of NFL teams.
    """
    data = make_request('draft/teams')
    return pd.DataFrame(data)


def get_nfl_positions():
    """
    Fetches a list of NFL positions.

    Returns:
        pd.DataFrame: A DataFrame containing a list of NFL positions.
    """
    data = make_request('draft/positions')
    return pd.DataFrame(data)


def get_nfl_draft_picks(year):
    """
    Fetches a list of NFL Draft picks for a specific year.

    Args:
        year (int): The year of the NFL Draft.

    Returns:
        pd.DataFrame: A DataFrame containing a list of NFL Draft picks.
    """
    data = make_request(f'draft/{year}/picks')
    return pd.DataFrame(data)

#_______________________________________________________________________________________________________________________________
