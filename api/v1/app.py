#!/usr/bin/python3
"""Creating Flask app instance, and returning it, with views
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


if __name__ == "__main__":
  env_host = getenv('HBNB_API_HOST', '0.0.0.0')
  env_port = int(getenv('HBNB_API_PORT', '5000'))
  app.run(host=env_host, port=env_port, threaded=True)