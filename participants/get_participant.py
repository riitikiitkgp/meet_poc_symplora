from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

get_participant_bp = Blueprint('get_participant', __name__)

@get_participant_bp.route('/conferenceRecords/<string:conferenceRecordId>/participant/<string:participant_id>', methods=['GET'])
def get_participant(conferenceRecordId, participant_id):
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }
        
    base_url = 'https://meet.googleapis.com/v2'
    participant_endpoint = f'{base_url}/conferenceRecords/{conferenceRecordId}/participants/{participant_id}'
    
    resp = requests.get(participant_endpoint, headers=headers)
    
    if resp.status_code == 401:  # Token expired or invalid
        return redirect(url_for('login'))
    
    return jsonify(resp.json())