#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import NotFound, BadRequest
from models import storage
from models.amenity import Amenity


@app_views.get('/amenities', strict_slashes=False)
def amenities():
    """return api status"""
    st = storage.all('Amenity').values()
    all_amenities = [v.to_dict() for v in st]
    return jsonify(all_amenities)


@app_views.get('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """return api status"""
    st = storage.get('Amenity', amenity_id)
    if st:
        return jsonify(st.to_dict())
    else:
        raise NotFound()


@app_views.delete('/amenities/<amenity_id>', strict_slashes=False)
def amenity_delete(amenity_id):
    st = storage.get('Amenity', amenity_id)
    if st:
        storage.delete(st)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.post('/amenities', strict_slashes=False)
def create_amenity():
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    obj = Amenity(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.put('/amenities/<amenity_id>', strict_slashes=False)
def update_amenity(amenity_id):
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    st = storage.get('Amenity', amenity_id)
    if not st:
        NotFound(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, v)
    st.save()
    return jsonify(st.to_dict()), 200
