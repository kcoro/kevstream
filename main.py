from flask import Flask, jsonify, redirect, render_template, session, url_for
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from os import environ as env
from functools import wraps
import json


# Flask app configuration
app = Flask(__name__, static_url_path='/static', static_folder='./static')
app.secret_key = 'ThisIsASecretKey'
app.debug = True


# auth0 configuration
AUTH0_CALLBACK_URL = 'https://kevstream.herokuapp.com/callback'
AUTH0_CLIENT_ID = 'akcunowK9MKZJD3sbouBNCNT15jx2bY6'
AUTH0_CLIENT_SECRET = 'N07vaTBfs--ZNk2jwsCMPfNgRZkmKJAVszb2kpzIMc4tlz8JhvdpP3WZBHqYN_k9'
AUTH0_DOMAIN = 'dev-jilpfaxm.us.auth0.com'
AUTH0_BASE_URL = 'https://dev-jilpfaxm.us.auth0.com'
AUTH0_AUDIENCE = 'https://kevstream.herokuapp.com.auth0.com/userinfo'
JWT_PAYLOAD = ''
PROFILE_KEY = ''


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

# Initialize auth0 object with settings
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# decorator for requiring authorization on routes
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Index base route
@app.route('/')
def index():
    return render_template('index.html')


# Route called by auth0, sends access token and acquires users data
# redirects user to /stream
@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[JWT_PAYLOAD] = userinfo
    session[PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
    }
    return redirect('/stream')


# route accessed via login button in index.html
# begins auth0 authentication process
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)


# Logs user out and reroutes to index page
@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


# Stream is only available to authenticated users
# auth0 /callback reroutes here on successfully authentication
@app.route('/stream')
@requires_auth
def dashboard():
    return render_template('stream.html',
                           userinfo=session[PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[JWT_PAYLOAD], indent=4))


