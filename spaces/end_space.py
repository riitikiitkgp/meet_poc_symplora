# Function to end an active conference
from flask import Flask, Blueprint, jsonify, request, redirect, url_for
from api_utils import load_token
import requests

end_space_bp = Blueprint('end_active_space', __name__)

@end_space_bp.route('/spaces/<string:space_id>/endActiveConference', methods=['POST'])
def end_active_conference(space_id):
    token = load_token()
    if not token:
        return redirect(url_for('login'))
    
    tok = token['access_token']
    
    headers = {
        'Authorization': f'Bearer {tok}',
        'Accept': 'application/json'
    }
    
    base_url = 'https://meet.googleapis.com/v2'
    end_conference_endpoint = f'{base_url}/spaces/{space_id}:endActiveConference'
    
    resp = requests.post(end_conference_endpoint, headers=headers)
    
    if resp.status_code == 401:  # Token expired or invalid
        return redirect(url_for('login'))
    
    return '', resp.status_code