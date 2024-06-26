import requests
import json
import os

def save_token(token):
    with open('token.json', 'w') as f:
        json.dump(token, f)

def load_token():
    if os.path.exists('token.json'):
        with open('token.json', 'r') as f:
            return json.load(f)
    return None

def make_authenticated_request(method, url, **kwargs):
    token = load_token()
    if not token:
        raise Exception("No token available. Please log in.")
    
    headers = kwargs.pop('headers', {})
    headers['Authorization'] = f"Bearer {token['access_token']}"
    
    response = requests.request(method, url, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()