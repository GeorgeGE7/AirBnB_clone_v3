#!/usr/bin/python3
"""users routs and functions to get users data from the API
"""
from flask import jsonify, abort, request
from models import storage, user
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """get all users from the storage
    """
    all_users = storage.all(user.User).values()
    return jsonify([user.to_dict() for user in all_users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """get a single user by a spacific id

    Args:
        user_id (int): user id

    Returns:
        object: userr object
    """
    single_user = storage.get(user.User, user_id)
    if single_user:
        return jsonify(single_user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """delete user by its id

    Args:
        user_id (int): user id

    Returns:
        obj: an empty object
    """
    to_be_deleted_user = storage.get(user.User, user_id)
    if to_be_deleted_user:
        storage.delete(to_be_deleted_user)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """create new user route

    Returns:
        object: the new created user
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if 'email' not in all_kwargs:
        return abort(400, 'Missing email')
    new_user = user.User(**all_kwargs)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """update existing aminity route

    Returns:
        object: the updated aminity object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    existing_user = storage.get(user.User, user_id)
    if existing_user:
        ignored_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in all_kwargs.items():
            if key not in ignored_keys:
                setattr(existing_user, key, value)
        storage.save()
        return jsonify(existing_user.to_dict()), 200
    else:
        return abort(404)
