#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import NotFound, BadRequest
from models import storage
from models.state import State


@app_views.get('/states', strict_slashes=False)
def states():
    """return api status"""
    st = storage.all('State').values()
    all_states = [v.to_dict() for v in st]
    return jsonify(all_states)


@app_views.get('/states/<state_id>')
def get_state(state_id):
    """return api status"""
    st = storage.get('State', state_id)
    if st:
        return jsonify(st.to_dict())
    else:
        raise NotFound()


@app_views.delete('/states/<state_id>', strict_slashes=False)
def state_delete(state_id):
    st = storage.get('State', state_id)
    if st:
        storage.delete(st)
        return jsonify({}), 200
    else:
        raise NotFound()


@app_views.post('/states', strict_slashes=False)
def create_state():
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.put('/states/<state_id>', strict_slashes=False)
def update_state(state_id):
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    st = storage.get('State', state_id)
    if not st:
        raise NotFound()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, v)
    st.save()
    return jsonify(st.to_dict()), 200
