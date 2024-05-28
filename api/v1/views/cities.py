#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import NotFound, BadRequest
from models import storage
from models.city import City


@app_views.get('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """return cities for a particular state_id status"""
    st = storage.get('State', state_id)
    if st:
        all_cities = st.cities
        new_list_of_objs = list(map(lambda obj: obj.to_dict(), all_cities))
        return jsonify(new_list_of_objs)
    else:
        raise NotFound()


@app_views.get('/cities/<city_id>')
def get_city(city_id):
    """get a city"""
    ct = storage.get('City', city_id)
    if ct:
        return jsonify(ct.to_dict())
    else:
        raise NotFound()


@app_views.delete('/cities/<city_id>', strict_slashes=False)
def city_delete(city_id):
    """deletes a city"""
    ct = storage.get('City', city_id)
    if ct:
        storage.delete(ct)
        return jsonify({}), 200
    else:
        raise NotFound()


@app_views.post('/states/<state_id>/cities', strict_slashes=False)
def create_city(state_id):
    """create a city object"""
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description="Missing name")
    st = storage.get('State', state_id)
    if st:
        obj = City(**data)
        obj.state_id = state_id
        obj.save()

        return jsonify(obj.to_dict()), 201
    else:
        raise NotFound()


@app_views.put('/cities/<city_id>', strict_slashes=False)
def update_city(city_id):
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')

    ct = storage.get('City', city_id)
    if not ct:
        raise NotFound()
    else:
        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(ct, k, v)
        ct.save()
        return jsonify(ct.to_dict()), 200
