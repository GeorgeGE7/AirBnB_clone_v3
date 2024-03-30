#!/usr/bin/python3
"""Cities routs and functions to get city/Cities data from the API
"""
from flask import jsonify, abort, request
from models import storage, state, city
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state_id(state_id):
    """get city by state id route

    Args:
        state_id (int): state id
    """
    state_by_id = storage.get(state.State, state_id)
    if not state_by_id:
        return abort(404)
    state_cities = [city.to_dict() for city in state_by_id.cities]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """get single city by id route

    Args:
        city_id (int): city id
    """
    city_by_id = storage.get(city.City, city_id)
    if city_by_id:
        return jsonify(city_by_id.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """delete single city by id route

    Args:
        city_id (int): city id
    """
    city_by_id = storage.get(city.City, city_id)
    if city_by_id:
        storage.delete(city_by_id)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city_by_state_id(state_id):
    """create city by state id route

    Args:
        state_id (int): state id
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state_by_id = storage.get(state.State, state_id)
    if not state_by_id:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if 'name' not in all_kwargs:
        return abort(400, 'Missing name')
    all_kwargs['state_id'] = state_id
    new_city = city.City(**all_kwargs)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """update single city by id route

    Args:
        city_id (int): city_id
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    existing_city = storage.get(city.City, city_id)
    if existing_city:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        new_data = request.get_json()
        ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in new_data.items():
            if key not in ignored_keys:
                setattr(existing_city, key, value)
        storage.save()
        return jsonify(existing_city.to_dict()), 200
    else:
        return abort(404)
