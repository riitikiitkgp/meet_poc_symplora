# Function to get a space by ID
from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

get_space_bp = Blueprint('get_space', __name__)

@get_space_bp.route('/spaces/<string:space_id>', methods=['GET'])
def get_space(space_id):
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }

    base_url = 'https://meet.googleapis.com/v2'
    space_endpoint = f'{base_url}/spaces/{space_id}'
    
    resp = requests.get(space_endpoint, headers=headers)
    
    if resp.status_code == 401:  # Token expired or invalid
        return redirect(url_for('login'))
    
    return jsonify(resp.json())