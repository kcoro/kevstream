This is a Flask project which uses auth0 as an Oauth2 service provider.
The application is a simple demonstration of configuring auth0 to protect routes in a flask application.
The app provides login with a valid google account, or the sample username and password account provided.
Protected routes include a buffered video stream as well as a route to a users live stream.

## To view this app running on Heroku:
[https://kevstream.herokuapp.com/](https://kevstream.herokuapp.com/)

## How to Implement
To implement this app:
- add your own auth0 secrets and credentials to main.py.
- edit live_stream.html, in the video element add your own ipaddress
