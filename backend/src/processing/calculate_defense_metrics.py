import pandas as pd

def pass_completion_percentage_allowed(plays_df):
    """
    Calculate the Pass Completion Percentage Allowed by the defense.

    This metric measures the percentage of completed passes by the opposing team's offense.

    Args:
    plays_df (pd.DataFrame): A pandas DataFrame containing the defensive plays.

    Returns:
    float: The calculated Pass Completion Percentage Allowed.
    """
    completed_passes = len(plays_df[(plays_df['play_type'] == 'Pass Reception') | (plays_df['play_type'] == 'Passing Touchdown')])
    pass_attempts = len(plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return'])])
    pass_completion_percentage_allowed = completed_passes / pass_attempts if pass_attempts > 0 else 0
    return pass_completion_percentage_allowed

def defensive_sack_rate(plays_df):
    """
    Calculate the Defensive Sack Rate.

    This metric measures the frequency at which the defense sacks the opposing quarterback as a percentage of passing plays.

    Args:
    plays_df (pd.DataFrame): A pandas DataFrame containing the defensive plays.

    Returns:
    float: The calculated Defensive Sack Rate.
    """
    sacks = len(plays_df[plays_df['play_type'] == 'Sack'])
    pass_plays = len(plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return', 'Sack'])])
    sack_rate = sacks / pass_plays if pass_plays > 0 else 0
    return sack_rate

def interception_rate(plays_df):
    """
    Calculate the Interception Rate.

    This metric measures the frequency at which the defense intercepts the opposing quarterback as a percentage of passing plays.

    Args:
    plays_df (pd.DataFrame): A pandas DataFrame containing the defensive plays.

    Returns:
    float: The calculated Interception Rate.
    """
    interceptions = len(plays_df[plays_df['play_type'] == 'Interception Return'])
    pass_attempts = len(plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return'])])
    interception_rate = interceptions / pass_attempts if pass_attempts > 0 else 0
    return interception_rate

def defensive_passer_rating(plays_df):
    """
    Calculate the Defensive Passer Rating.

    This metric assesses the overall efficiency of the defense against the pass, taking into account completion percentage, yards per attempt, touchdown rate, and interception rate.

    Args:
    plays_df (pd.DataFrame): A pandas DataFrame containing the defensive plays.

    Returns:
    float: The calculated Defensive Passer Rating.
    """
    completed_passes = len(plays_df[(plays_df['play_type'] == 'Pass Reception') | (plays_df['play_type'] == 'Passing Touchdown')])
    pass_attempts = len(plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return'])])
    passing_yards = plays_df.loc[(plays_df['play_type'] == 'Pass Reception') | (plays_df['play_type'] == 'Passing Touchdown'), 'yards_gained'].sum()
    passing_touchdowns = len(plays_df[plays_df['play_type'] == 'Passing Touchdown'])
    interceptions = len(plays_df[plays_df['play_type'] == 'Interception Return'])

    comp_pct = (completed_passes / pass_attempts) * 100 if pass_attempts > 0 else 0
    yards_per_attempt = passing_yards / pass_attempts if pass_attempts > 0 else 0
    td_rate = (passing_touchdowns / pass_attempts) * 100 if pass_attempts > 0 else 0
    int_rate = (interceptions / pass_attempts) * 100 if pass_attempts > 0 else 0

    passer_rating = ((comp_pct * 0.3) + (yards_per_attempt * 0.25) + (td_rate * 0.2) - (int_rate * 0.45)) * 100 / 6

    return passer_rating

def opponents_passing_play_success_rate(plays_df):
    """
    Calculate the Opponent's Passing Play Success Rate.

    This metric evaluates the efficiency of the passing defense by measuring the percentage of successful passing plays by the opponent.

    Args:
    plays_df (pd.DataFrame): A pandas DataFrame containing the defensive plays.

    Returns:
    float: The calculated Opponent's Passing Play Success Rate.
    """
    successful_passes = len(plays_df[((plays_df['play_type'].isin(['Pass Reception', 'Passing Touchdown'])) & (plays_df['yards_gained'] >= plays_df['distance'] / 2) & (plays_df['down'] == 1)) | ((plays_df['yards_gained'] >= plays_df['distance'] * 0.7) & (plays_df['down'].isin([2, 3, 4])))])
    pass_attempts = len(plays_df[plays_df['play_type'].isin(['Pass Reception', 'Pass Incompletion', 'Passing Touchdown', 'Interception Return'])])
    passing_play_success_rate = successful_passes / pass_attempts if pass_attempts > 0 else 0
    return passing_play_success_rate
