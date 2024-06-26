#Function to get conference by its ID
from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

get_conference_bp = Blueprint('get_conference', __name__)

@get_conference_bp.route('/conferenceRecords/<string:conferenceRecordId>', methods=['GET'])
def get_conference(conference_id):
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }

    base_url = 'https://meet.googleapis.com/v2'
    conference_endpoint = f'{base_url}/conferenceRecords/{conference_id}'
    
    resp = requests.get(conference_endpoint, headers=headers)
    
    if resp.status_code == 401:
        return redirect(url_for('login'))
    
    return jsonify(resp.json())