from flask import request, jsonify
from src.internal_api.queries import get_top_qbs_overall, get_top_qbs_by_week, query_firestore_player_data, get_qb_by_name
from src.internal_api import app
from src.api import data_requests as dr
from src.api.data_requests import search_player
from src.utils import utils, gcp_utils as gutils
import pandas as pd
from flask_cors import CORS, cross_origin
CORS(app, support_credentials=True, )
from ariadne import load_schema_from_path
import os

@app.route('/conferences', methods=['GET'])
def get_conferences():
    conference = dr.get_fbs_teams(2022)[['school', 'conference']]
    result = conference.to_dict('records')
    return jsonify(result)

@app.route('/player_meta', methods=['GET'])
def get_meta_data():
    player_name = request.args.get('player_name')
    result = search_player(player_name).to_dict('records')[0]
    return jsonify(result)


@app.route('/overall_rankings_player', methods=['GET'])
def overall_rankings_player():
    player_name = request.args.get('player_name')
    result = get_qb_by_name(player_name)
    return jsonify(result)

@app.route('/player_data', methods=['GET'])
def get_player_data():
    player_name = request.args.get('player_name')
    year = int(request.args.get('year'))
    result = query_firestore_player_data(player_name, year)
    result = [{k: ('' if isinstance(v, str) else 0) if pd.isna(v) or v is None else v for k, v in d.items()} for d in result]

    # print(type(result))
    return jsonify(result)


@app.route('/overall_rankings_top', methods=['GET'])
def get_overall_rankings():
    top_x = int(request.args.get('top_x'))
    field = request.args.get('field')
    result = get_top_qbs_overall(top_x, field)
    return jsonify(result)


def get_weekly_rankings():
    top_x = int(request.args.get('top_x'))
    week = request.args.get('week')
    result = get_top_qbs_by_week(week, top_x)
    return jsonify(result)

from google.cloud import firestore

@app.route('/weekly_rankings', methods=['GET'])
def query_top_qb_weekly_performances():
    """
    Query the top documents from the 'qb' collection based on 'qb_total_score'.
    
    Parameters:
    limit (int): Number of top documents to return.

    Returns:
    List[Dict[str, Any]]: A list of dictionaries representing the top documents.
    """
    # Reference the 'qb' collection
    db = gutils.get_firestore_client_db()
    limit = int(request.args.get('top_x'))

    qb_ref = db.collection("qb")
    top_documents = qb_ref.order_by("qb_total_score", direction=firestore.Query.DESCENDING).limit(limit).stream()
    top_document_dicts = [doc.to_dict() for doc in top_documents]
    return top_document_dicts

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = '0.0.0.0'
    app.run(host=host, port=port, debug=True)


    # app.run(debug=True)


# def get_top_qb_game_performances(limit):
#     # Create a Firestore client
#     db = gutils.get_firestore_client_db()

#     # Query the 'qb' collection, sorted by the 'qb_total_score' field in descending order
#     # and limit the results to the top `limit` scores
#     docs_ref = db.collection('qb').order_by('qb_total_score', direction=firestore.Query.DESCENDING).limit(limit)

#     # Get the documents
#     docs = docs_ref.get()

#     # Return the documents as a list
#     return [doc.to_dict() for doc in docs]