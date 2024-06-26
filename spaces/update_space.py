# Function to update a space
from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

update_space_bp = Blueprint('update_space', __name__)

@update_space_bp.route('/spaces/<string:space_id>', methods=['PATCH'])

def update_space(space_id):
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }

    base_url = 'https://meet.googleapis.com/v2'
    update_space_endpoint = f'{base_url}/spaces/{space_id}'
    
    space_data = request.json
    params = {
        'updateMask': request.args.get('updateMask', '*')
    }
    resp = requests.patch(update_space_endpoint, json=space_data, params=params, headers=headers)
    
    if resp.status_code == 401:  # Token expired or invalid
        return redirect(url_for('login'))
    
    return jsonify(resp.json()), resp.status_code