#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import NotFound, BadRequest
from models import storage
from models.user import User


@app_views.get('/users', strict_slashes=False)
def users():
    """get all users"""
    users = storage.all(User).values()
    all_users = [user.to_dict() for user in users]
    return jsonify(all_users)


@app_views.get('/users/<user_id>')
def get_user(user_id):
    """get a user"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        raise NotFound()


@app_views.delete('/users/<user_id>', strict_slashes=False)
def user_delete(user_id):
    """delete a user"""
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        return jsonify({}), 200
    else:
        raise NotFound()


@app_views.post('/users', strict_slashes=False)
def create_user():
    """create a user"""
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description="Missing email")
    if 'password' not in data:
        raise BadRequest(description="Missing password")

    obj = User(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.put('/users/<user_id>', strict_slashes=False)
def update_user(user_id):
    """update a user"""
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    user = storage.get(User, user_id)
    if not user:
        raise NotFound()
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
