#!/usr/bin/python3
"""Creating Flask app instance, and returning it, with views
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """This method calls storage.close() at the end of each request"""
    storage.close()

@app.errorhandler(404)
def not_found_error_handler():
    """This method for 404 error - Not found page"""   
    res = {"error": "Not found"}
    return jsonify(res), 404 


if __name__ == "__main__":
    env_host = getenv('HBNB_API_HOST', '0.0.0.0')
    env_port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=env_host, port=env_port, threaded=True)