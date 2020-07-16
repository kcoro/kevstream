from flask import Flask, request, url_for, render_template, jsonify, redirect, session
from werkzeug.utils import secure_filename
from markupsafe import escape
# auth0 requirements
import json
from functools import wraps
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
	'auth0',
	client_id='akcunowK9MKZJD3sbouBNCNT15jx2bY6',
	client_secret='N07vaTBfs--ZNk2jwsCMPfNgRZkmKJAVszb2kpzIMc4tlz8JhvdpP3WZBHqYN_k9',
	api_base_url='https://dev-jilpfaxm.us.auth0.com',
	access_token_url='https://dev-jilpfaxm.us.auth0.com/oauth/token',
	authorize_url='https://dev-jilpfaxm.us.auth0.com/authorize',
	client_kwargs={
	'scope': 'openid profile email',
	},
)


# Check if user is authenticated, use it to decorate methods
# that require authentication
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)
  return decorated


# Index contains link to /login route to begin authentication
@app.route('/')
def index():
	return render_template('index.html')


# auth0 callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/stream')


#  Login uses AuthLib client to redirect user to login page.
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://kevstream.herokuapp.com/callback')


# Logout users via auth0
@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'akcunowK9MKZJD3sbouBNCNT15jx2bY6'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


# Successful authentication will reroute user to main stream.
@app.route('/stream')
@requires_auth
def stream():
    return render_template('stream.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


