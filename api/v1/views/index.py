#!/usr/bin/python3
"""Creating Flask index for views - app_views
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """get the api status - json format
    """
    res={"status": "OK"}
    return jsonify(res)


app_views.route('/stats')
def get_stats_count():
    """method that gets states count
    """
    re_stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "place": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(re_stats)
