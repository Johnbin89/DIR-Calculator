from flask import request

from app import db
from app.api import api_bp
from app.minimum_gas.diveplan import min_gas_bar
from app.minimum_gas.validation import (
    plan_warning,
    read_int,
    read_tank,
    validate_plan_input,
)
from app.minimum_gas.views import create_plan, get_hash
from app.models import ShareLink


def plan_response(depth, gas, solve, tank=24):
    plan, _, bar, litres, time_to_fs, _ = create_plan(depth, gas, solve, tank)
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
    depth, solve, gas, tank, errors = validate_plan_input(request.get_json(silent=True) or {})
    if errors:
        return {'errors': errors}, 422
    warning = plan_warning(depth, gas)
    if warning:
        return {'warning': warning}, 422
    return plan_response(depth, gas, solve, tank)


@api_bp.post('/gas-used')
def gas_used():
    data = request.get_json(silent=True) or {}
    errors = {}
    litres = read_int(data, 'litres', errors)
    tank = read_tank(data, 'tank', errors)
    if errors:
        return {'errors': errors}, 422
    return {'bar': min_gas_bar(litres, tank), 'selected_tank': tank}


@api_bp.post('/share')
def share():
    depth, solve, gas, _, errors = validate_plan_input(request.get_json(silent=True) or {})
    if errors:
        return {'errors': errors}, 422
    warning = plan_warning(depth, gas)
    if warning:
        return {'warning': warning}, 422
    hash = get_hash()
    db.session.add(ShareLink(depth=depth, gas=gas, solve=solve, hash=hash))
    db.session.commit()
    return {'hash': hash}


@api_bp.get('/share/<hash>')
def shared_plan(hash):
    sharedplan = db.session.scalars(db.select(ShareLink).filter_by(hash=hash)).first()
    if sharedplan is None:
        return {'error': 'Shared plan not found'}, 404
    return {'hash': hash, **plan_response(sharedplan.depth, sharedplan.gas, sharedplan.solve)}
