from flask import jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_states():
    """ Retrieves a list of all State objects. """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieves a specific State object by state_id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object by state_id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State object. """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    new_state = State(**request.get_json())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
