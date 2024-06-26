import os
import json
from flask import Flask, Blueprint, jsonify, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from api_utils import save_token, load_token

from spaces.create_space import create_space_bp
from spaces.get_space import get_space_bp
from spaces.update_space import update_space_bp
from spaces.end_space import end_space_bp
from participants.list_participants import list_participants_bp
from participants.get_participant import get_participant_bp
from conferences.list_conferences import list_conferences_bp
from conferences.get_conference import get_conference_bp

app = Flask(__name__)
app.secret_key = 'aafa11332e7047a9b4039a50cd726ca3790df50b677ff5704e6d12b91c51e402'

app.register_blueprint(create_space_bp)
app.register_blueprint(get_space_bp)
app.register_blueprint(update_space_bp)
app.register_blueprint(end_space_bp)
app.register_blueprint(list_conferences_bp)
app.register_blueprint(get_conference_bp)
app.register_blueprint(get_participant_bp)
app.register_blueprint(list_participants_bp)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='5123480394-t8edh6inn53bcen8dkkrtb820r8eb8qc.apps.googleusercontent.com',
    client_secret='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',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:2000/authorize',
    client_kwargs={'scope': 'https://www.googleapis.com/auth/meetings.space.readonly https://www.googleapis.com/auth/meetings.space.created'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    save_token(token)
    session['token'] = token
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('token', None)
    if os.path.exists('token.json'):
        os.remove('token.json')
    return redirect(url_for('index'))

@app.route('/')
def index():
    token = load_token()
    if token:
        session['token'] = token
        return 'Logged in'
    else:
        return 'Not logged in'

if __name__ == '__main__':
    app.run(port=2000, debug=True)
