from backend.src.utils import utils
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

def read_qb_usage_csv(team_name):
    file_path = os.environ.get("LOCAL_QB_USAGE_PATH")
    file_name = f"{team_name}.csv"
    full_path = f"{file_path}/{file_name}"
    
    try:
        qb_usage_df = pd.read_csv(full_path)
        return qb_usage_df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    

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
    if week is None:
        raise ValueError("Error: No week specified")

    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('plays', params=params)

    if not data:
        raise ValueError(f"Error: No data found for year {year}, team {team}, and week {week}")

    df = pd.DataFrame(data)

    # assign week column to df from input param
    df['week'] = week
    df['team'] = team
    df['year'] = year
    return df


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


def read_team_roster_csv(team, year=2022):
    if year != 2022:
        print("Only 2022 rosters are available.")
        return None
    base_folder = os.environ.get('LOCAL_ROSTER_PATH')
    file_name = f"{team}.csv"
    full_path = os.path.join(base_folder, file_name)
    
    try:
        roster_df = pd.read_csv(full_path)
        return roster_df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
read_team_roster_csv('Michigan')

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


# RANKINGS 
# _________________________________________________________________

def get_rankings(year=None, week=None):
    """
    Fetches historical polls and rankings for a given year and week.

    Args:
        year (int, optional): The year of the season.
        week (int, optional): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing historical poll rankings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('rankings', params=params)
    dfs = [pd.DataFrame(poll['ranks'])[['rank', 'school', 'conference', 'firstPlaceVotes', 'points']] for poll_data in data for poll in poll_data['polls']]
    df = pd.concat(dfs, ignore_index=True)
    df['year'] = year
    df['week'] = week
    return df

# BETTING 
def get_betting_lines(gameId=None, year=None, week=None, seasonType=None, team=None):
    """
    Fetches betting lines for a given year and season type.

    Args:
        year (int, optional): The year of the season.
        season_type (str, optional): The season type (regular, postseason, etc.).

    Returns:
        pd.DataFrame: A DataFrame containing betting lines.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('lines', params=params)
        
    dfl=[]
    for game in data:
        df = pd.DataFrame(game['lines'])
        df['season'] = game['season']
        df['week'] = game['week']
        df['homeTeam'] = game['homeTeam']
        df['awayTeam'] = game['awayTeam']
        df['homeScore'] = game['homeScore']
        df['awayScore'] = game['awayScore']
        dfl.append(df)

    return_df = pd.concat(dfl, ignore_index=True)
    return return_df

# RECRUITING 
# _________________________________________________________________
def get_player_recruiting(year=None, classification=None, position=None, state=None, team=None):
    """
    Fetches player recruiting ratings and rankings for a given year.

    Args:
        year (int, optional): The year of the recruiting cycle.

    Returns:
        pd.DataFrame: A DataFrame containing player recruiting ratings and rankings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('recruiting/players', params=params)
    return pd.DataFrame(data)


def get_team_recruiting(year=None, team=None):
    """
    Fetches team recruiting rankings and ratings for a given year.

    Args:
        year (int, optional): The year of the recruiting cycle.

    Returns:
        pd.DataFrame: A DataFrame containing team recruiting rankings and ratings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('recruiting/teams', params=params)
    return pd.DataFrame(data)


def get_recruit_position_ratings(startYear=None, endYear=None, team=None, conference=None):
    """
    Fetches recruit position group ratings for a given year.

    Args:
        year (int, optional): The year of the recruiting cycle.

    Returns:
        pd.DataFrame: A DataFrame containing recruit position group ratings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('recruiting/groups', params=params)
    return pd.DataFrame(data)

# RATINGS 
# _________________________________________________________________

def get_sp_ratings(year=None, team=None):
    """
    Fetches historical SP+ ratings for a given year and week.

    Args:
        year (int, optional): The year of the season.
        week (int, optional): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing historical SP+ ratings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ratings/sp', params=params)
    df = pd.DataFrame(data)
    offense_df = pd.json_normalize(df['offense']).add_prefix('offense_')
    defense_df = pd.json_normalize(df['defense']).add_prefix('defense_')
    special_teams_df = pd.json_normalize(df['specialTeams']).add_prefix('specialTeams_')
    threshold = int(0.95 * len(df))
    flattened_df = pd.concat([df.drop(['offense', 'defense', 'specialTeams'], axis=1), offense_df, defense_df, special_teams_df], axis=1).dropna(thresh=threshold, axis=1)
    return flattened_df


def get_srs_ratings(year=None, week=None):
    """
    Fetches historical SRS ratings for a given year and week.

    Args:
        year (int, optional): The year of the season.
        week (int, optional): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing historical SRS ratings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ratings/srs', params=params)
    return pd.DataFrame(data)


def get_sp_conference_ratings(year=None, conference=None):
    """
    Fetches historical SP+ ratings by conference for a given year and conference.

    Args:
        year (int, optional): The year of the season.
        conference (str, optional): The conference to retrieve SP+ ratings for.

    Returns:
        pd.DataFrame: A DataFrame containing historical SP+ ratings by conference.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ratings/sp/conferences', params=params)
    return pd.DataFrame(data)


def get_elo_ratings(year=None, week=None):
    """
    Fetches historical Elo ratings for a given year and week.

    Args:
        year (int, optional): The year of the season.
        week (int, optional): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing historical Elo ratings.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ratings/elo', params=params)
    return pd.DataFrame(data)

# METRICS 
def get_predicted_points(down=None, distance=None):
    """
    Fetches predicted points (i.e. expected points or EP) for a given down and distance.

    Args:
        year (int, optional): The year of the season.
        week (int, optional): The week of the season.

    Returns:
        pd.DataFrame: A DataFrame containing predicted points data.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ppa/predicted', params=params)
    return pd.DataFrame(data)

def get_ppa_teams(year=None, team=None, conference=None):
    """
    Fetches predicted points added (PPA/EPA) data by team for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing PPA/EPA data by team.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ppa/teams', params=params)
    return pd.DataFrame(data)


def get_ppa_games(year=None, week=None, team=None, conference=None):
    """
    Fetches team predicted points added (PPA/EPA) by game for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing team PPA/EPA data by game.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ppa/games', params=params)
    return pd.DataFrame(data)


def get_ppa_player_games(year=None, week=None, team=None, conference=None, position=None, playerId=None):
    """
    Fetches player predicted points added (PPA/EPA) broken down by game for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing player PPA/EPA data broken down by game.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ppa/players/games', params=params)
    return pd.DataFrame(data)


def get_ppa_player_season(year=None, week=None, team=None, conference=None, position=None, playerId=None):
    """
    Fetches player predicted points added (PPA/EPA) broken down by season for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing player PPA/EPA data broken down by season.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('ppa/players/season', params=params)
    return pd.DataFrame(data)


def get_win_probability(gameId):
    """
    Fetches win probability chart data for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing win probability chart data.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('metrics/wp', params=params)
    return pd.DataFrame(data)


def get_pregame_win_probability(year=None, week=None, team=None, seasonType=None):
    """
    Fetches pregame win probability data for a given year.

    Args:
        year (int, optional): The year of the season.

    Returns:
        pd.DataFrame: A DataFrame containing pregame win probability data.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request('metrics/wp/pregame', params=params)
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


def get_nfl_draft_picks(year=None, nflTeam=None, college=None, position=None, conference=None):
    """
    Fetches a list of NFL Draft picks for a specific year.

    Args:
        year (int): The year of the NFL Draft.

    Returns:
        pd.DataFrame: A DataFrame containing a list of NFL Draft picks.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    data = make_request(f'draft/picks', params=params)
    return pd.DataFrame(data)