#!/usr/bin/python3
""" task 11 """
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places_of_city(city_id):
    """
        Retrieves the list of all Place objects of a City
    """
    for city in storage.all(City).values():
        if city.id == city_id:
            list_of_cities = []
            for place in storage.all(Place).values():
                if place.city_id == city_id:
                    list_of_cities.append(place.to_dict())
            return jsonify(list_of_cities)
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def all_places(place_id):
    """
        Retrieves a Place object
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
        Deletes a Place object
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            storage.delete(place)  # delete the place
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
        Creates a Place
    """
    from models.user import User
    first_check = storage.get(City, city_id)
    if not first_check:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    for city in storage.all(City).values():
        if city.id == city_id:  # si encuentra una ciudad
            for user in storage.all(User).values():
                if user.id == data['user_id']:  # si encuentra un usuario
                    place = Place(**data)
                    place.save()
                    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
        Updates a Place
    """
    first_check = storage.get(Place, place_id)
    if not first_check:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    list_to_ignore = ['id', 'user_id', 'place_id',
                      'created_at', 'update_at', 'city_id']
    for place in storage.all(Place).values():
        if place.id == place_id:  # si encuentro un place
            for k, v in data.items():
                if k not in list_to_ignore:
                    setattr(place, k, v)
            storage.save()  # saves the changes
            return make_response(jsonify(place.to_dict()), 200)
