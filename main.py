from flask import Flask, jsonify, redirect, render_template, session, url_for
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from os import environ as env
from functools import wraps
import json


AUTH0_CALLBACK_URL = 'https://kevstream.herokuapp.com/callback'
AUTH0_CLIENT_ID = 'akcunowK9MKZJD3sbouBNCNT15jx2bY6'
AUTH0_CLIENT_SECRET = 'N07vaTBfs--ZNk2jwsCMPfNgRZkmKJAVszb2kpzIMc4tlz8JhvdpP3WZBHqYN_k9'
AUTH0_DOMAIN = 'dev-jilpfaxm.us.auth0.com'
AUTH0_BASE_URL = 'https://dev-jilpfaxm.us.auth0.com'
AUTH0_AUDIENCE = 'https://kevstream.herokuapp.com.auth0.com/userinfo'
JWT_PAYLOAD = ''
PROFILE_KEY = ''


app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = 'ThisIsASecretKey'
app.debug = True


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

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


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[JWT_PAYLOAD] = userinfo
    session[PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session[PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[JWT_PAYLOAD], indent=4))


