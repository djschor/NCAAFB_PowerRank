import pandas as pd

import ast

from concurrent.futures import ThreadPoolExecutor
from backend.src.processing import score_qb_metrics as sqm
import numpy as np 
def adaptive_quarterback_score(plays_df):
    """
    Adaptive Quarterback Score: The Adaptive Quarterback Score (AQS) is a composite metric that evaluates a quarterback's adaptability, timing, and proficiency in various game scenarios. It takes into account completion percentage, situational pass success rate, third-down conversion efficiency, and weighted throw variety, providing a comprehensive view of a quarterback's performance.

    Args:
    completion_percentage (float): Completion percentage of the quarterback.
    situational_pass_success_rate (float): Success rate of passes in third-down situations.
    third_down_conversion_eff (float): Efficiency in converting third downs.
    weighted_throw_variety (float): Ratio of passing touchdowns to total passing attempts.

    Returns:
    float: The calculated alternative Adaptive Quarterback Score (AQS).
    """
    # Filter plays for pass attempts
    pass_attempts = plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return'])]

    # Compute completions, attempts, and passing touchdowns
    completions = len(pass_attempts[(pass_attempts['play_type'] == 'Pass Reception') | (pass_attempts['play_type'] == 'Passing Touchdown')])
    attempts = len(pass_attempts)
    passing_touchdowns = len(pass_attempts[pass_attempts['play_type'] == 'Passing Touchdown'])

    # Compute third down attempts and conversions
    third_down_attempts_df = pass_attempts[(pass_attempts['down'] == 3) & (pass_attempts['play_type'].isin(['Pass Reception', 'Passing Touchdown']))]
    third_down_attempts = len(third_down_attempts_df)
    third_down_conversions = len(third_down_attempts_df[third_down_attempts_df['yards_gained'] >= third_down_attempts_df['distance']])

    # Calculate metrics
    completion_percentage = completions / attempts if attempts > 0 else 0
    situational_pass_success_rate = third_down_conversions / third_down_attempts if third_down_attempts > 0 else 0
    third_down_conversion_efficiency = third_down_conversions / third_down_attempts if third_down_attempts > 0 else 0
    weighted_throw_variety = passing_touchdowns / attempts if attempts > 0 else 0

    # Compute AQS
    aqs = (completion_percentage + situational_pass_success_rate + third_down_conversion_efficiency + weighted_throw_variety) / 4
    return aqs * 100


def quarterback_passing_index(plays_df):
    """
    Quarterback Passing Index: The Quarterback Passing Index (QPI) measures a quarterback's passing performance by considering completion percentage, yards per attempt, touchdown ratio, and interception ratio. This index provides a balanced evaluation of a quarterback's ability to complete passes, gain yards, score touchdowns, and avoid interceptions.

    Args:
    completion_percentage (float): Completion percentage of the quarterback.
    yards_per_attempt (float): Average yards per attempt.
    touchdown_ratio (float): Touchdown-to-attempt ratio.
    interception_ratio (float): Interception-to-attempt ratio.

    Returns:
    float: The calculated Quarterback Performance Index (QPI).
    """
    relevant_play_types = ('Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return')
    
    # Filter the DataFrame for relevant play types
    filtered_plays = plays_df[plays_df['play_type'].isin(relevant_play_types)]

    # Calculate aggregated statistics
    attempts = len(filtered_plays)
    completions = len(filtered_plays[(filtered_plays['play_type'] == 'Pass Reception') | (filtered_plays['play_type'] == 'Passing Touchdown')])
    passing_yards = filtered_plays['yards_gained'].sum()
    touchdowns = len(filtered_plays[filtered_plays['play_type'] == 'Passing Touchdown'])
    interceptions = len(filtered_plays[filtered_plays['play_type'] == 'Interception Return'])

    completion_percentage = completions / attempts if attempts > 0 else 0
    yards_per_attempt = passing_yards / attempts if attempts > 0 else 0
    touchdown_ratio = touchdowns / attempts if attempts > 0 else 0
    interception_ratio = interceptions / attempts if attempts > 0 else 0
    qpi = (completion_percentage + yards_per_attempt + touchdown_ratio - interception_ratio) / 4
    return qpi * 100



def scramble_efficiency_index(plays_df):
    scramble_yards = plays_df.loc[plays_df['play_type'] == 'Rush', 'yards_gained'].sum()
    scramble_attempts = plays_df['play_type'].eq('Rush').sum()

    sei = scramble_yards / scramble_attempts if scramble_attempts > 0 else 0
    return sei * 100

def completion_rate_above_expected(plays_df):
    completed_passes = plays_df['play_type'].isin(['Pass Reception', 'Passing Touchdown']).sum()
    pass_attempts = plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return']).sum()

    actual_completion_rate = completed_passes / pass_attempts if pass_attempts > 0 else 0

    completed_passes_ppa = plays_df.loc[plays_df['play_type'].isin(['Pass Reception', 'Passing Touchdown']), 'ppa'].astype(float).sum()
    expected_completion_rate = completed_passes_ppa / pass_attempts if pass_attempts > 0 else 0

    expected_completion_rate = np.clip(expected_completion_rate, 0, 1)

    crae = actual_completion_rate - expected_completion_rate
    return crae * 100

def decision_making_index(plays_df):
    completed_passes = plays_df['play_type'].isin(['Pass Reception', 'Passing Touchdown']).sum()
    interceptions = plays_df['play_type'].eq('Interception Return').sum()
    sacks = plays_df['play_type'].eq('Sack').sum()
    fumbles = plays_df['play_type'].eq('Fumble Recovery (Opponent)').sum()

    total_plays = completed_passes + interceptions + sacks + fumbles
    dmi = (completed_passes - interceptions - sacks - fumbles) / total_plays if total_plays > 0 else 0
    return dmi * 100

#_____

def pressure_performance_index(plays_data):
    if plays_data.empty:
        return None

    pressure_weights = {
        "down": 0.13,
        "time": 0.12,
        "defense": 0.03,
        "yards_weighted_score": 0.20,
        "ppa_score": 0.06,
        "first_down_score": 0.20,
        "completion_score": 0.13,
        "sack_score": 0.13
    }

    plays_data['distance_score'] = (1 - (plays_data['yards_to_goal'] / 100)) * 100
    plays_data['down_score'] = (plays_data['down'] / 4) * 100
    plays_data['time_remaining'] = plays_data['clock'].apply(lambda x: ast.literal_eval(x)['minutes'] * 60 + ast.literal_eval(x)['seconds'])
    plays_data['time_score'] = (1 - (plays_data['time_remaining'] / (4 * 15 * 60))) * 100
    plays_data['average_defense_score'] = plays_data.apply(lambda row: sqm.get_opponent_defense_metrics(row['defense'], row['week'], row['year']) if row['defense'] and row['week'] and row['year'] else np.nan, axis=1)
    plays_data['yards_weighted_scoring_score'] = 0.6 * (plays_data['scoring'] * 100) + 0.4 * plays_data['yards_gained']
    plays_data['completion_score'] = (0.9 * (plays_data['play_type'] == 'Pass Reception') * 100) + 0.5 * plays_data['yards_gained']
    plays_data['sack_score'] = np.where(plays_data['play_type'] == 'Sack', 0, 100)
    plays_data['ppa_score'] = plays_data['ppa'].apply(lambda x: (1 - float(x)) * 100 if x is not None else np.nan)
    plays_data['first_down_score'] = np.where(plays_data['yards_gained'] >= plays_data['distance'], 100, 0)

    plays_data['pressure_score'] = (
        pressure_weights["down"] * plays_data['down_score']
        + pressure_weights["time"] * plays_data['time_score']
        + pressure_weights["defense"] * plays_data['average_defense_score']
        + pressure_weights["yards_weighted_score"] * plays_data['yards_weighted_scoring_score']
        + pressure_weights["ppa_score"] * plays_data['ppa_score']
        + pressure_weights["first_down_score"] * plays_data['first_down_score']
        + pressure_weights["completion_score"] * plays_data['completion_score']
        + pressure_weights["sack_score"] * plays_data['sack_score']
    )

    ppi = plays_data['pressure_score'].mean()

    return ppi






def adjusted_deep_pass_success_rate(plays, touchdown_weight=4, interception_weight=4, adjustment_factor=0.1):
    """
    Adjusted Deep Pass Success Rate (ADPSR): This metric evaluates a quarterback's performance on deep pass plays (20 yards or more) 
    by taking into account touchdowns, interceptions, and the number of deep pass attempts. The formula is adjusted to prevent extreme 
    values when the sample size is small.

    Args:
    plays (DataFrame): A dataframe containing the play data.
    touchdown_weight (int): The weight assigned to touchdowns in the formula. Default is 4.
    interception_weight (int): The weight assigned to interceptions in the formula. Default is 4.
    adjustment_factor (float): The adjustment factor for small sample sizes. Default is 0.1.

    Returns:
    float: The calculated Adjusted Deep Pass Success Rate (ADPSR) as a percentage.
    """

    if plays.empty or 'play_text' not in plays.columns:
        return None

    deep_pass_attempts = len(plays[(plays.play_type == 'Pass Reception') | (plays.play_type == 'Pass Incompletion')])
    deep_pass_touchdowns = len(plays[(plays.play_type == 'Pass Reception') & (plays.yards_gained >= 20)])
    deep_pass_interceptions = len(plays[(plays.play_type == 'Interception')])

    adjusted_touchdowns = deep_pass_touchdowns + adjustment_factor * touchdown_weight
    adjusted_interceptions = deep_pass_interceptions + adjustment_factor * interception_weight

    adpsr = (adjusted_touchdowns - adjusted_interceptions) / (deep_pass_attempts + touchdown_weight + interception_weight)

    return adpsr * 100


def red_zone_efficiency_rating(plays):
    """
    Red Zone Efficiency Rating: The Red Zone Efficiency Rating (RZER) quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone. This rating is useful for evaluating a quarterback's ability to capitalize on scoring opportunities and make critical plays near the end zone.

    Args:
    red_zone_touchdowns (int): Total number of touchdowns scored inside the red zone.
    red_zone_attempts (int): Total number of red zone attempts.

    Returns:
    float: The calculated Red Zone Efficiency Rating (RZER).
    """
    red_zone_attempts = len(plays[plays.yards_to_goal <= 20])
    red_zone_touchdowns = len(plays[(plays.play_type.str.contains('Touchdown')) & (plays.yards_to_goal <= 20)])
    if red_zone_attempts == 0:
        return 0
    else:
        rzer = (red_zone_touchdowns / red_zone_attempts) * 100
        return rzer