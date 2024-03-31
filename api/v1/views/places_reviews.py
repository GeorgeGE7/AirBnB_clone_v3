#!/usr/bin/python3
"""Cities routs and functions to get city/Cities data from the API
"""
from flask import jsonify, abort, request
from models import storage, place, review, review, user
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_places_reviews_id(place_id):
    """get places review by id route

    Args:
        place_id (int): place id
    """
    existing_place = storage.get(place.Place, place_id)
    if not existing_place:
        return abort(404)
    p_r_list = [riview.to_dict() for riview in existing_place.reviews]
    return jsonify(p_r_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_reviews_id(review_id):
    """get review by id route

    Args:
        review_id (int): review id
    """
    existing_review = storage.get(review.Review, review_id)
    if not existing_review:
        return abort(404)
    return jsonify(existing_review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews_id(review_id):
    """delete review by id route

    Args:
        review_id (int): review id
    """
    existing_review = storage.get(review.Review, review_id)
    if not existing_review:
        return abort(404)
    storage.delete(existing_review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_reviews(place_id):
    """delete review by id route

    Args:
        place_id (int): place id
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    existing_place = storage.get(place.Place, place_id)
    if not existing_place:
        return abort(404)
    all_kwargs = request.get_json()
    if 'user_id' not in all_kwargs.keys():
        return abort(400, 'Missing user_id')
    if not storage.get(user.User, all_kwargs['user_id']):
        return abort(404)
    if 'text' not in all_kwargs.keys():
        return abort(400, 'Missing text')
    new_place = place.Place(**all_kwargs)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """update existing review route

    Returns:
        object: the updated review object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    existing_re = storage.get(review.Review, review_id)
    if existing_re:
        ignored_keys = ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']
        for key, value in all_kwargs.items():
            if key not in ignored_keys:
                setattr(existing_re, key, value)
        storage.save()
        return jsonify(existing_re.to_dict()), 200
    else:
        return abort(404)
