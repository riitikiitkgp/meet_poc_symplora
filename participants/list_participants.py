from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from authlib.integrations.flask_client import OAuth
from api_utils import load_token
import requests

list_participants_bp = Blueprint('list_participants', __name__)

@list_participants_bp.route('/conferenceRecords/<string:conferenceRecordId>/participants', methods=['GET'])
def list_participants(conferenceRecordId):
    token = load_token()
    if not token:
        return redirect(url_for('login'))

    base_url = 'https://meet.googleapis.com/v2'
    conference_endpoint = f'{base_url}/conferenceRecords/{conferenceRecordId}/participants'

    params = {
        'pageSize': request.args.get('pageSize', 100),
        'pageToken': request.args.get('pageToken', ''),
        'filter': request.args.get('filter', ''),
    }

    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }

    # Make the GET request to the Google Meet API
    resp = requests.get(conference_endpoint, headers=headers, params=params)

    # Check for token expiration or invalid token
    if resp.status_code == 401:
        return redirect(url_for('login'))

    # Return the JSON response from the Google Meet API
    return jsonify(resp.json())