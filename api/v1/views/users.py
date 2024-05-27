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
    st = storage.all('User').values()
    all_users = [v.to_dict() for v in st]
    return jsonify(all_users)


@app_views.get('/users/<user_id>')
def get_user(user_id):
    """get a user"""
    st = storage.get('User', user_id)
    if st:
        return jsonify(st.to_dict())
    else:
        raise NotFound()


@app_views.delete('/users/<user_id>', strict_slashes=False)
def user_delete(user_id):
    """delete a user"""
    st = storage.get('User', user_id)
    if st:
        storage.delete(st)
        return jsonify({}), 200
    else:
        abort(404)


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
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    st = storage.get('User', user_id)
    if not st:
        NotFound(404)
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(st, k, v)
    st.save()
    return jsonify(st.to_dict()), 200
