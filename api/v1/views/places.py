#!/usr/bin/python3
"""Cities routs and functions to get city/Cities data from the API
"""
from flask import jsonify, abort, request
from models import storage, place, city, user, state, amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city_id(city_id):
    """get places by city id route

    Args:
        city_id (int): state id
    """
    city_by_id = storage.get(city.City, city_id)
    if not city_by_id:
        return abort(404)
    city_places = [place.to_dict() for place in city_by_id.places.values()]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """get single place by id route

    Args:
        place_id (int): place id
    """
    place_by_id = storage.get(place.Place, place_id)
    if place_by_id:
        return jsonify(place_by_id.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """delete single place by id route

    Args:
        place_id (int): place id
    """
    place_by_id = storage.get(place.Place, place_id)
    if place_by_id:
        storage.delete(place_by_id)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place_by_city_id(city_id):
    """create place by city id route

    Args:
        city_id (int): city id
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city_by_id = storage.get(city.City, city_id)
    if not city_by_id:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if 'user_id' not in all_kwargs.keys():
        return abort(400, 'Missing user_id')
    if not storage.get(user.User, all_kwargs['user_id']):
        return abort(404)
    if 'name' not in all_kwargs:
        return abort(400, 'Missing name')
    all_kwargs['city_id'] = city_id
    new_place = place.Place(**all_kwargs)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """update single place by id route

    Args:
        place_id (int): place_id
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    existing_place = storage.get(place.Place, place_id)
    if existing_place:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        new_data = request.get_json()
        ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in new_data.items():
            if key not in ignored_keys:
                setattr(existing_place, key, value)
        storage.save()
        return jsonify(existing_place.to_dict()), 200
    else:
        return abort(404)


@app_views.route('/places_search', strict_slashes=False)
def serach_for_place():
    """search for place route
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    all_kwargs = request.get_json()
    if all_kwargs:
        user_input_s = all_kwargs.get('states')
        user_input_c = all_kwargs.get('cities')
        user_input_a = all_kwargs.get('amenities')
    if not (user_input_a or user_input_c or user_input_s):
        places_search = storage.all(place.Place).values()
        p_s_list = [place_s.to_dict() for place_s in places_search]
        return jsonify(p_s_list)
    p_s_list = []
    if user_input_s:
        all_states = [storage.get(state.State, s_id) for s_id in user_input_s]
        for sstate in all_states:
            if sstate:
                for scity in sstate.cities:
                    if scity:
                        for splace in scity.places:
                            p_s_list.append(splace)
    if user_input_c:
        all_cities = [storage.get(city.City, c_id) for c_id in user_input_c]
        for scity in all_cities:
            if scity:
                for splace in scity.places:
                    if splace not in p_s_list:
                        p_s_list.append(splace)

    if user_input_a:
        if not p_s_list:
            all_places = storage.all(place.Place).values()
            all_amies = [storage.get(amenity.Amenity) for am_id in user_input_a]
            for splace in all_places:
                if all(am in splace.amenities for am in all_amies):
                    p_s_list.append(splace)
    f_places = []
    for spo in p_s_list:
        spd = spo.to_dict()
        spd.pop('amenities', None)
        f_places.append(spd)
    return jsonify(f_places)