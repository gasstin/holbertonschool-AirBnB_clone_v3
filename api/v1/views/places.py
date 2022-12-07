#!/usr/bin/python3
""" task 11 """
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models.city import City
from models.place import Place
from models import storage

@app_views.route('/api/v1/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places_of_city(city_id):
    """
        Retrieves the list of all Place objects of a City
    """
    for city in storage.all(City):
        if city.id == city_id:
            list_of_cities = [place.to_dict() for place in storage.all(Place)
                              if place.city_id == city_id]
            return jsonify(list_of_cities)
    abort(404)


@app_views.route('/api/v1/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def all_places(place_id):
    """
        Retrieves a Place object
    """
    for place in storage.all(Place):
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/api/v1/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
        Deletes a Place object
    """
    for place in storage.all(Place):
        if place.id == place_id:
            storage.delete(place)
            return {}, 200
    abort(404)


@app_views.route('/api/v1/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
        Creates a Place
    """
    from models.user import User
    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    for city in storage.all(City):
        if city.id == city_id: # si encuentra una ciudad
            for user in storage.all(User):
                if user.id == data['user_id']: # si encuentra un usuario
                    place = Place(data)
                    return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/api/v1/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
        Updates a Place
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for place in storage.all(Place):
        if place.id == place_id: # si encuentro un place
            for k,v in data.items():
                if k not in ['id', 'created_at', 'update_at', 'city_id']:
                    place.k = v
            return place, 200
    abort(404)