#Function to list conferences
from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from authlib.integrations.flask_client import OAuth
from api_utils import load_token
from flask import current_app
import requests

list_conferences_bp = Blueprint('list_conferences', __name__)

@list_conferences_bp.route('/conferenceRecords', methods = ['GET'])
def list_conferences():
    token = load_token()

    tok = token['access_token']

    if not token:
        return redirect(url_for('login'))
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }
    

    base_url = 'https://meet.googleapis.com/v2'
    conferences_endpoint = f'{base_url}/conferenceRecords'
    
    resp = requests.get(conferences_endpoint, headers=headers)
    print(resp)
    # if resp.status_code == 401:
    #     return redirect(url_for('login'))
    
    return jsonify(resp.json())