from flask import Flask, request, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)

# Index page will default to login page and validate user credentials.
# Successful authentication will reroute user to homepage.
@app.route('/')
def homepage():
	return '<h1>HOMEPAGE</h1>'

# API v1 route
@app.route('/api/v1')
def apiv1():
	return jsonify(sensorData)

# Fake sensor data for API testing
sensorData = [
	       {
		 'name': 'indoorSensor',
		 'id': 0,
		 'temperature': 76,
		 'humiditiy': 52
	       },
	       {
		 'name': 'outdoorSensor',
		 'id': 1,
		 'temperature': 88,
		 'humidity': 85
	       }
	     ]


