#!/usr/bin/python3
"""states routs and functions to get state/states data from the API
"""
from flask import jsonify, abort, request
from models import storage, state
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_states():
    """get all states or get single state if id is specified
    """
    all_states = storage.all(state.State).values()
    all_states_list = [state.to_dict() for state in all_states]
    return jsonify(all_states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states_by_id(state_id):
    """get state by a spacific id
    """
    single_state = storage.get(state.State, state_id)
    if single_state:
        return jsonify(single_state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states_by_id(state_id):
    """delete a state by a spacific id
    """
    to_be_deleted_state = storage.get(state.State, state_id)
    if to_be_deleted_state:
        storage.delete(to_be_deleted_state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    """create a new state route
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if 'name' not in all_kwargs:
        abort(400, 'Missing name')

    new_state = state.State(**all_kwargs)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """update state data by id route
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    existing_state = storage.get(state.State, state_id)
    if existing_state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        new_data = request.get_json()
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key, value in new_data.items():
            if key not in ignored_keys:
                setattr(existing_state, key, value)
        storage.save()
        return jsonify(existing_state.to_dict()), 200
    else:
        return abort(404)
