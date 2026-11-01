from flask import request

from app import db
from app.api import api_bp
from app.models import ShareLink, generate_share_hash
from app.planning.diveplan import calculate_plan, min_gas_bar
from app.planning.validation import (
    plan_warning,
    read_int,
    read_tank,
    validate_plan_input,
)


def json_object():
    """Return the request's JSON object, or {} for any other body so validation rejects it."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def plan_response(depth, gas, solve, tank=24):
    plan, bar, litres, time_to_fs = calculate_plan(depth, gas, solve, tank)
    return {
        'depth': depth,
        'gas': gas,
        'solve': solve,
        'tank': tank,
        'plan': [stop.to_dict() for stop in plan],
        'litres': litres,
        'bar': bar,
        'time_to_fs': time_to_fs,
    }


@api_bp.post('/minimum-gas')
def minimum_gas():
    depth, solve, gas, tank, errors = validate_plan_input(json_object())
    if errors:
        return {'errors': errors}, 422
    warning = plan_warning(depth, gas)
    if warning:
        return {'warning': warning}, 422
    return plan_response(depth, gas, solve, tank)


@api_bp.post('/gas-used')
def gas_used():
    data = json_object()
    errors = {}
    litres = read_int(data, 'litres', errors)
    tank = read_tank(data, 'tank', errors)
    if errors:
        return {'errors': errors}, 422
    return {'bar': min_gas_bar(litres, tank), 'selected_tank': tank}


@api_bp.post('/share')
def share():
    depth, solve, gas, tank, errors = validate_plan_input(json_object())
    if errors:
        return {'errors': errors}, 422
    warning = plan_warning(depth, gas)
    if warning:
        return {'warning': warning}, 422
    hash = generate_share_hash()
    db.session.add(ShareLink(depth=depth, gas=gas, solve=solve, tank=tank, hash=hash))
    db.session.commit()
    return {'hash': hash}


@api_bp.get('/share/<hash>')
def shared_plan(hash):
    sharedplan = db.session.scalars(db.select(ShareLink).filter_by(hash=hash)).first()
    if sharedplan is None:
        return {'error': 'Shared plan not found'}, 404
    return {'hash': hash, **plan_response(sharedplan.depth, sharedplan.gas, sharedplan.solve, sharedplan.tank)}
