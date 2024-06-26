from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

create_space_bp = Blueprint('create_space', __name__)

@create_space_bp.route('/spaces', methods=['POST'])
def create_space():
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }

    base_url = 'https://meet.googleapis.com/v2'
    spaces_endpoint = f'{base_url}/spaces'
    
    space_data = request.json
    resp = requests.post(spaces_endpoint, json=space_data)
    
    if resp.status_code == 401:  # Token expired or invalid
        return redirect(url_for('login'))
    
    return jsonify(resp.json()), resp.status_code