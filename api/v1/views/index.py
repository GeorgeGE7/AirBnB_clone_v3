#!/usr/bin/python3
"""Creating Flask index for views - app_views
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """get the api status - json format
    """
    res={"status": "OK"}
    return jsonify(res)