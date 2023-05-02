
import pandas as pd
import numpy as np 
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import requests
import time
from decimal import Decimal 
from google.cloud import firestore
import datetime as DT
from concurrent.futures import ThreadPoolExecutor
import functools
import io
import math
import datetime
from tqdm import tqdm

def scan_firestore_collection(collection_name):
    """
    Queries Firestore and retrieves all documents in the specified collection.
    
    Args:
        collection_name (str): The name of the Firestore collection to query.
            - Options:  'qbs', 
                        'defense', 
                        'meta', 
                        'qb_overall_rankings_2022'   
                        'qb_weekly_rankings_2022
    """
    try:
        # Initialize Firestore client
        db = get_firestore_client_db()

        # Get the collection reference
        collection_ref = db.collection(collection_name)

        # Stream all documents in the collection
        docs = collection_ref.stream()

        # Convert each document to a dictionary and add it to the results list
        results = [doc.to_dict() for doc in docs]

        return results

    except Exception as e:
        print(f"Error querying all documents in {collection_name}: {e}")
        return []

def query_firestore_general(collection_name, pk):
    """
    Queries Firestore for data in collections where the primary key (pk) is specified directly,
    such as the meta table.
    
    Args:
        collection_name (str): The name of the Firestore collection to query.
        pk (str): The primary key of the document to retrieve.
    
    Returns:
        dict: A dictionary representing the document with the specified primary key if it exists, None otherwise.
    """
    try:
        # Initialize Firestore client
        db = get_firestore_client_db()
        print(pk)

        # Get the collection reference
        collection_ref = db.collection(collection_name)

        # Retrieve the document using the primary key (pk)
        doc_ref = collection_ref.document(str(pk))
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            print(f"No document found in {collection_name} with pk {pk}")
            return None

    except Exception as e:
        print(f"Error querying {collection_name} with pk {pk}: {e}")
        return None


def query_firestore_player_data(collection_name, player_name, year):
    """
    Queries the 'qb' collection in Firestore to get quarterback weekly performance data,
    where the primary key (pk) is formatted like <player_name>_week_year.

    Args:
        collection_name (str): The name of the Firestore collection to query.
        player_name (str): The name of the quarterback.
        year (int): The year of the quarterback's performance data.

    Returns:
        list: A list of dictionaries representing the documents with the specified player name and year if any exist, None otherwise.
    """
    try:
        # Initialize Firestore client
        db = get_firestore_client_db()

        # Get the collection reference
        collection_ref = db.collection(collection_name)

        # Query the collection for documents with the specified player name and year
        query = collection_ref.where('player', '==', player_name).where('year', '==', year)
        docs = query.stream()

        results = []
        for doc in docs:
            if doc.exists:
                results.append(doc.to_dict())

        if not results:
            print(f"No documents found in {collection_name} for player {player_name} and year {year}")
            return None

        return results

    except Exception as e:
        print(f"Error querying {collection_name} for player {player_name} and year {year}: {e}")

def query_firestore(collection_name, team, week, year):
    """
    Queries a Firestore collection with a primary key (pk) formatted like <team>_<week>_<year>,
    which is suitable for collections where team, week, and year are specified, such as the 'qb' and 'defense' collections.

    Args:
        collection_name (str): The name of the Firestore collection to query.
        team (str): The name of the team.
        week (int): The week of the season.
        year (int): The year of the data.

    Returns:
        dict: A dictionary representing the queried document if it exists, None otherwise.
    """
    # Initialize Firestore client
    db = get_firestore_client_db()
    pk = f"{team}_{week}_{year}"

    # Get the collection reference
    collection_ref = db.collection(collection_name)

    # Retrieve the document using the primary key (pk)
    doc_ref = collection_ref.document(pk)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No document found in {collection_name} with pk {pk}")
        return None


def get_project_path():
    """
    Returns the absolute path of the project directory.
    """
    # return str(Path(__file__).parent.parent.parent)
    return str(Path(__file__).parent.parent.parent.parent)

def get_firestore_client_db():
    """
    Returns a Firestore client instance using the service account credentials JSON file.

    Note: Change the 'cred_file_path' variable to the absolute path of your Firebase credentials.
    """
    cred_file_path = os.environ.get('FIRESTORE_CRED_FILE_PATH')
    db = firestore.Client.from_service_account_json(cred_file_path)
    return db


def batch_save_data_firestore(data, table, id=None):
    """
    Saves data to a Firestore collection in a batch. Must have a unique identifier.

    :param data: A Pandas DataFrame or list of dictionaries containing the data to be saved.
    :param table: A string specifying the Firestore collection to save the data in.
    :param id: A string specifying the column name to be used as the document ID. Defaults to None.
    """
    if isinstance(data, pd.DataFrame):
        data = data.to_dict('records')

    def chunk_divisions(length, max_chunk_size=500):
        """
        Calculates the number of chunks to divide the input data based on the maximum chunk size.

        :param length: The length of the input data.
        :param max_chunk_size: The maximum size of each chunk. Defaults to 500.
        :return: The number of chunks to divide the input data.
        """
        return -(-length // max_chunk_size)

    chunk_items = np.array_split(data, chunk_divisions(len(data)))
    for item in chunk_items:
        db = get_firestore_client_db()
        collection = db.collection(table)
        batch = db.batch()

        def add_to_batch(batch, item):
            if id is None:
                doc_id = item['symbol']
            else:
                doc_id = item[id]
            new_doc_ref = collection.document(doc_id)
            batch.set(new_doc_ref, item)

        try:
            with ThreadPoolExecutor() as executor:
                with tqdm(total=len(item), desc=f"Saving {len(item)} to {table} collection") as pbar:
                    for _ in executor.map(functools.partial(add_to_batch, batch), item):
                        pbar.update()

            batch.commit()
            print(f"Successfully saved {len(item)} to {table} collection")
        except Exception as e:
            print(f"Error saving {len(item)} to {table}: {e}")

    return

def save_data_to_firestore(data, db, table):
    """
    Saves a single item to a Firestore collection. Must have a symbol unique identifier.

    :param data: A dictionary containing the data to be saved.
    :param db: A Firestore database client instance.
    :param table: A string specifying the Firestore collection to save the data in.
    """
    symbol = data['symbol']
    doc_ref = db.collection(table).document(symbol)
    try:
        doc_ref.set(data)
        print('Successfully saved {} to {} collection'.format(symbol, table))
    except Exception as e:
        print('Error saving {} to {}: {}'.format(symbol, table, e))

def update_firestore_document(data: dict, table: str):
    """
    Updates the document in the Google Cloud Firestore corresponding to the specified collection and document ID.

    :param data: A dictionary containing the data to update. The 'symbol' key in the dictionary should contain the document ID.
    :param table: A string specifying the Firestore collection to update the document in.
    """
    # Initialize the Firestore client
    db = firestore.Client()

    # Retrieve the document reference using the collection and document ID
    symbol = data['symbol']
    doc_ref = db.collection(table).document(symbol)

    # Update the document with the new data
    try:
        doc_ref.update(data)
        print(f"Successfully updated document {symbol} in collection {table}")
    except Exception as e:
        print(f"Error updating document {symbol} in collection {table}: {e}")


''' 
Beginning utils functions for tables that do not have a symbol unique identifier, such as the Analytics table 
'''

def save_data_to_firestore_id(data, db, table, id):
    """
    Saves a single item to a Firestore collection. Must have a symbol unique identifier.

    :param data: A dictionary containing the data to be saved.
    :param db: A Firestore database client instance.
    :param table: A string specifying the Firestore collection to save the data in.
    """
    doc_ref = db.collection(table).document(id)
    try:
        doc_ref.set(data)
        print('Successfully saved {} to {} collection'.format(id, table))
    except Exception as e:
        print('Error saving {} to {}: {}'.format(id, table, e))


def update_firestore_document_id(data: dict, table: str, id: str):
    """
    Updates the document in the Google Cloud Firestore corresponding to the specified collection and document ID.

    :param data: A dictionary containing the data to update. The 'symbol' key in the dictionary should contain the document ID.
    :param table: A string specifying the Firestore collection to update the document in.
    """
    # Initialize the Firestore client
    db = firestore.Client()

    # Retrieve the document reference using the collection and document ID
    doc_ref = db.collection(table).document(id)

    # Update the document with the new data
    try:
        doc_ref.update(data)
        print(f"Successfully updated document {id} in collection {table}")
    except Exception as e:
        print(f"Error updating document {id} in collection {table}: {e}")

def chunk_divisions(num):
    target_size = 500
    min_num_divs = math.ceil(num / target_size)
    max_num_divs = math.ceil(num / (target_size - 1))
    
    for num_divs in range(min_num_divs, max_num_divs + 1):
        div_size = math.ceil(num / num_divs)
        excess = (num_divs * div_size) - num
        if excess <= div_size:
            return num_divs
    return max_num_divs

