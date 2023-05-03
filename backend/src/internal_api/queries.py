import pandas as pd 
import numpy as np
import os
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
# import utils as utils located as src/utils/utils.py
from backend.src.utils import utils, gcp_utils as gutils
from backend.src.api import data_requests as dr
from backend.src.processing import calculate_qb_metrics as cqm, calculate_defense_metrics as cdm, score_defense_metrics as sdm, score_qb_metrics as sqm
from concurrent.futures import ThreadPoolExecutor, as_completed
from retry import retry
import functools
from multiprocessing import Pool
from google.cloud import firestore

def get_qb_by_name(qb_name, collection_name="qb_overall_rankings_2022"):
    """
    Queries Firestore collection "qb_overall_rankings_2022" and returns the quarterback with the specified name.

    Args:
        qb_name (str): The name of the quarterback to search for.
        collection_name (str): The name of the Firestore collection containing the QB data.

    Returns:
        dict: Dictionary containing the QB data if found, or an error message if not found.
    """
    try:
        # Initialize Firestore client
        db = gutils.get_firestore_client_db()

        # Query the Firestore collection for the specified quarterback
        query = db.collection(collection_name).where("player", "==", qb_name).stream()

        # Retrieve the document from the query
        qb_data = [doc.to_dict() for doc in query]

        # Check if the quarterback is found
        if len(qb_data) == 0:
            return {"success": False, "errors": [f"No quarterback found with the name '{qb_name}'"], "data": []}

        return qb_data[0]

    except Exception as e:
        print(f"Error fetching quarterback by name: {e}")
        return {"success": False, "errors": [f"Error fetching quarterback by name: {e}"], "data": []}


def get_top_qbs_overall(top_x, field='avg_qb_total_score'):
    """
    Queries Firestore collection "qb_overall_rankings_2022" and returns the top X QBs based on the specified field.

    Args:
        top_x (int): The number of top QBs to return.
        field (str): The field name to sort the QBs by (e.g., 'avg_qb_competitive_score', 'avg_qb_total_score', 'competitive_score_rank', or 'total_score_rank').

    Returns:
        List[dict]: List of dictionaries containing top X QBs data.
    """
    if field not in {'avg_qb_competitive_score', 'avg_qb_total_score', 'competitive_score_rank', 'total_score_rank'}:
        return {"success": False, "errors": [f"Invalid field '{field}'. Valid fields are: 'avg_qb_competitive_score', 'avg_qb_total_score', 'competitive_score_rank', and 'total_score_rank'."], "data": []}

    collection_name = "qb_overall_rankings_2022"
    top_x = int(top_x)
    try:
        # Initialize Firestore client
        db = gutils.get_firestore_client_db()

        # Query the Firestore collection, order by the specified field, and limit the results to top X
        query = db.collection(collection_name).order_by(field, direction=firestore.Query.DESCENDING if field.startswith('avg_') else firestore.Query.ASCENDING).limit(top_x).stream()

        # Retrieve all documents from the query
        top_qbs = [doc.to_dict() for doc in query]

        return top_qbs

    except Exception as e:
        print(f"Error fetching top QBs overall: {e}")
        return {"success": False, "errors": [f"Error fetching top QBs overall: {e}"], "data": []}


def get_top_qbs_by_week(week, top_x):
    """
    Queries Firestore collection "qb_weekly_rankings_2022" and returns the top X QBs by week.
    
    Args:
        week (int): The week number to filter results.
        top_x (int): The number of top QBs to return.

    Returns:
        List[dict]: List of dictionaries containing top X QBs data.
    """
    collection_name = "qb_weekly_rankings_2022"

    try:
        # Initialize Firestore client
        db = gutils.get_firestore_client_db()

        # Query the Firestore collection for documents with the specified week and order by qb_total_score
        query = db.collection(collection_name).where("week", "==", week).order_by("qb_total_score", direction=firestore.Query.DESCENDING).limit(top_x).stream()

        # Retrieve all documents from the query
        top_qbs = [doc.to_dict() for doc in query]

        return top_qbs

    except Exception as e:
        print(f"Error fetching top QBs by week: {e}")
        return {"success": False, "errors": [f"Error fetching top QBs by week: {e}"], "data": []}


def query_firestore_player_data(player_name, year):
    try:
        collection_name = 'qb'

        # Initialize Firestore client
        db = gutils.get_firestore_client_db()

        # Get the collection reference
        collection_ref = db.collection(collection_name)

        # Query the collection for documents with the specified player name and year
        query = collection_ref.where(u'player', '==', player_name).where(u'year', u'==', year)
        docs = query.stream()

        results = []
        for doc in docs:
            if doc.exists:
                results.append(doc.to_dict())

        if not results:
            print(f"No documents found in {collection_name} for player {player_name} and year {year}")
            return ['']
        print(f"Successfully queried {collection_name} for player {player_name} and year {year}")
        return results

    except Exception as e:
        print(f"Error querying {collection_name} for player {player_name} and year {year}: {e}")
        return ['error']