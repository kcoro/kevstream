from flask import Flask, request, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def homepage():
	return '<h1>HOMEPAGE</h1>'


