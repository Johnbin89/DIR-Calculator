from flask import current_app, request
from flask_socketio import emit, join_room, leave_room

from app import db, socketio
from app.models import ShareLink
from app.planning.diveplan import calculate_plan, min_gas_bar
from app.planning.validation import (
    plan_warning,
    read_int,
    read_tank,
    validate_plan_input,
)


@socketio.on('shared_tank_change')
def shared_tank_change(data):
    # print(f"Tank change event: {data}")
    errors = {}
    selected_tank = read_tank(data, 'selected_tank', errors)
    litres = read_int(data, 'min_gas_l', errors)
    if errors:
        return
    sharedplan = ShareLink.query.filter_by(hash=data.get('room')).first()
    if sharedplan is None:
        return
    sharedplan.tank = selected_tank
    db.session.commit()
    bar = min_gas_bar(litres, selected_tank)
    emit('shared_tank_change', ({'bar':bar, 'selected_tank': selected_tank}), to=data['room'])


@socketio.on('plan_change')
def plan_change(data):
    # print(f"Plan change event: {data}")
    depth, solve, gas, selected_tank, errors = validate_plan_input({
        'depth': data.get('new_depth'),
        'solve': data.get('new_solve_time'),
        'gas': data.get('new_gas'),
        'tank': data.get('selected_tank'),
    })
    if errors or plan_warning(depth, gas):
        return
    sharedplan = ShareLink.query.filter_by(hash=data['room']).first_or_404()
    plan, bar, litres, time_to_fs = calculate_plan(depth, gas, solve, selected_tank)
    sharedplan.depth = depth
    sharedplan.gas = gas
    sharedplan.solve = solve
    sharedplan.tank = selected_tank
    db.session.commit()
    json_plan = [stop.to_dict() for stop in plan]
    emit('plan_change', ({'depth': data['new_depth'], 'gas': data['new_gas'], 'solve': data['new_solve_time'],
                          'bar':bar, 'selected_tank': selected_tank,
                          'time_to_fs': time_to_fs, 'new_plan': json_plan, 'litres': litres,}),
         to=data['room'])


@socketio.on('join')
def join(room):
    print("Join")
    username=request.sid
    join_room(room['room'])
    module_socketio = current_app.extensions['socketio']
    participants_generator = module_socketio.server.manager.get_participants(request.namespace ,room['room'])
    participants = [a for a,b in participants_generator]
    #print(participants, len(participants))
    emit('join', (username+" entered the room", len(participants)-1), to=room['room'])


@socketio.on('leave')
def leave(room):
    print("leave")
    username=request.sid
    leave_room(room['room'])
    module_socketio = current_app.extensions['socketio']
    participants_generator = module_socketio.server.manager.get_participants(request.namespace ,room['room'])
    participants = [a for a,b in participants_generator]
    #print(participants, len(participants))
    emit('leave', (username+" left the room", len(participants)-1), to=room['room'])
