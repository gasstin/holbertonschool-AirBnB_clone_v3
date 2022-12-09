#!/usr/bin/python3
""" task 12 """
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews_of_place(place_id):
    """
        Retrieves the list of all Place objects of a City
    """
    for place in storage.all(Place).values():
        if place.id == place_id:  # if find a place
            list_of_reviews = [review.to_dict() for review
                               in storage.all(Review).values()
                               if review.place_id == place_id]
            return jsonify(list_of_reviews)
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def all_reviews(review_id):
    """
        Retrieves a Review object
    """
    for review in storage.all(Review).values():
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
        Deletes a Review object
    """
    for review in storage.all(Review).values():
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
        Creates a Place
    """
    from models.user import User
    place_check = storage.get(Place, place_id)
    if not place_check:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data = request.get_json()
    user_check = storage.get(User, data['user_id'])
    if not user_check:  # check if the user exists
        abort(404)
    for place in storage.all(Place).values():
        if place.id == place_id:  # si encuentra un place
                data['place_id'] = place_id
                review = Review(**data)  # Create a review
                review.save()
                return make_response(jsonify(review.to_dict()), 201)
    abort(404)


@app_views.route('reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
        Updates a Place
    """
    first_check = storage.get(Review, review_id)
    if not first_check:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    list_to_ignore = ['id', 'user_id', 'place_id',
                      'created_at', 'update_at']
    data = request.get_json()
    for review in storage.all(Review).values():
        if review.id == review_id:  # if match the review
            for k, v in data.items():
                if k not in list_to_ignore:
                    setattr(review, k, v)
            storage.save()  # saves the changes
            return make_response(jsonify(review.to_dict(), 200))
    abort(404)
