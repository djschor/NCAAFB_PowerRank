import os
from retry import retry
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import pandas as pd 
import numpy as np
import os
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
# import utils as utils located as src/utils/utils.py
from backend.src.utils import utils, gcp_utils as gutils
from backend.src.api import data_requests as dr
from backend.src.processing import calculate_qb_metrics as cqm, calculate_defense_metrics as cdm, score_defense_metrics as sdm, score_qb_metrics as sqm
from backend.src.processing import score_qb_metrics as sqm
from concurrent.futures import ThreadPoolExecutor, as_completed
from retry import retry
@retry(tries=1, delay=30, backoff=30, jitter=(1, 3))
def get_plays_with_retry(year, team, week):
    try:
        plays = dr.get_plays(year=year, team=team, week=week)
        return plays
    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")
        raise

def save_plays_for_team_and_week(item):
    year, team, week = item
    # plays = get_plays_with_retry(year, team, week)
    base_folder = os.environ.get('LOCAL_PLAYS_PATH')
    try:
        plays = dr.get_plays(year=year, team=team, week=week)
    except Exception as e: 
        print(f"{e}")
    if not plays.empty:
        file_path = os.path.join(base_folder, f"{team}_{week}.csv")
        plays.to_csv(file_path, index=False)
        print(f"Saved plays for {team} in week {week} to {file_path}")
    else:
        print(f"No plays found for {team} in week {week}")

def save_team_plays_to_csv(year, max_workers=5):
    fbs_teams = dr.get_fbs_teams(season=year)
    team_names = fbs_teams['school'].tolist()[4:]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [(year, team, week) for team in team_names for week in range(1, 15)]
        res = executor.map(save_plays_for_team_and_week, tasks)
    x = list(res)
    return
    # with (max_workers=max_workers) as executor:
    #     for team in team_names:
    #         for week in range(1, 15):  # Assuming 14 weeks in the season
    #             executor.submit(save_plays_for_team_and_week, year, team, week)


@retry(tries=1, delay=30, backoff=30, jitter=(1, 3))
def get_team_roster_with_retry(team_name, year):
    try:
        roster = dr.get_team_rosters(team_name, year)
        return roster
    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")
        raise

def save_roster_for_team(item):
    year, team_name = item
    base_folder = os.environ.get('LOCAL_ROSTER_PATH')

    try:
        roster = get_team_roster_with_retry(team_name, year)
    except Exception as e:
        print(f"{e}")

    if not roster.empty:
        file_path = os.path.join(base_folder, f"{team_name}.csv")
        roster.to_csv(file_path, index=False)
        print(f"Saved roster for {team_name} to {file_path}")
    else:
        print(f"No roster found for {team_name}")

def save_team_rosters_to_csv(year, max_workers=5):
    fbs_teams = dr.get_fbs_teams(season=year)
    team_names = fbs_teams['school'].tolist()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [(year, team_name) for team_name in team_names]
        res = executor.map(save_roster_for_team, tasks)

    x = list(res)
    return


def save_qb_usage_to_csv(year, team_name):
    base_folder = os.environ.get('LOCAL_QB_USAGE_PATH')
    qb_usage = dr.get_player_usage(year, team=team_name, position='QB')

    if not qb_usage.empty:
        file_path = os.path.join(base_folder, f"{team_name}.csv")
        qb_usage.to_csv(file_path, index=False)
        print(f"Saved QB usage for {team_name} to {file_path}")
    else:
        print(f"No QB usage found for {team_name}")

def save_all_teams_qb_usage_to_csv(year):
    fbs_teams = dr.get_fbs_teams(season=year)
    team_names = fbs_teams['school'].tolist()

    for team_name in team_names:
        save_qb_usage_to_csv(year, team_name)

