#!/usr/bin/python3
"""amenities routs and functions to get amenities data from the API
"""
from flask import jsonify, abort, request
from models import storage, amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    all_am = storage.get(amenity.Amenity).values()
    all_am_list = [single_amenity.to_dict() for single_amenity in all_am]
    return jsonify(all_am_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    single_amenity = storage.get(amenity.Amenity, amenity_id)
    if single_amenity:
        return jsonify(single_amenity.to_dict())
    else:
        return abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    to_be_deleted_aminity = storage.get(amenity.Amenity, amenity_id)
    if to_be_deleted_aminity:
        storage.delete(to_be_deleted_aminity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if 'name' not in all_kwargs:
        abort(400, 'Missing name')
    new_amenity = amenity.Amenity(**all_kwargs)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    existing_amenity = storage.get(amenity.Amenity, amenity_id)
    if existing_amenity:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        all_kwargs = request.get_json()
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key, value in all_kwargs.items():
            if key not in ignored_keys:
                setattr(existing_amenity, key, value)
        storage.save()
        return jsonify(existing_amenity.to_dict()), 200
    else:
        return abort(404)
