#!/usr/bin/python3
"""
Create a new Place object handling default
RESTFul API actions
"""

from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves a list of all Place objects. """
    places = storage.get(City, city_id)
    if places is None:
        abort(404)
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a specific Place object by place_id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object by place_id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object. """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_place = request.get_json()
    city = storage.get(City, city_id)
    user = storage.get(User, new_place['user_id'])
    if city is None or user is None:
        abort(404)
    new_place['city_id'] = city.id
    new_place['user_id'] = user.id
    place = Place(**new_place)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save(place)
    return jsonify(place.to_dict()), 200
