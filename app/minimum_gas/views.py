from flask import render_template, session, redirect, url_for, flash, current_app, request
from app.minimum_gas import minimum_gas_bp
from app import db, socketio  
from app.minimum_gas.forms import DiveForm, ShareForm, TankForm
from app.minimum_gas.diveplan import min_gas_plan, min_gas_litres, min_gas_bar
from app.models import ShareLink
from flask_socketio import emit, join_room, leave_room



@minimum_gas_bp.route('/minimum-gas', methods=['GET', 'POST'])
@minimum_gas_bp.route('/minimum-gas/<hash>')
def minimum_gas(hash=None):
    def create_plan():
        plan = min_gas_plan(depth, gas_switch, solve)
        time_to_fs = plan[1].get_time() - solve   #time need from depth to first stop
        print(plan)
        litres = min_gas_litres(plan)
        bar = min_gas_bar(litres, 24)
        tank_form = TankForm(tank=24, min_gas_L = litres)
        share_form = ShareForm(depth = depth, solve = solve, gas_switch = gas_switch)
        return plan,tank_form, bar, litres, time_to_fs, share_form
    form = DiveForm()
    if form.validate_on_submit():
        depth = form.depth.data
        gas_switch = int(form.gas.data)
        if depth > 70:
            flash('That deep with available just a 50% is not wise')
            return render_template('minimum_gas/min_gas.html', form=form)
        if gas_switch == 0 and depth > 30:
            flash('Better take a stage, if you want to go below 30 meters.')
            return render_template('minimum_gas/min_gas.html', form=form)
        solve = form.solve.data
        #print(depth, gas_switch)
        plan, tank_form, bar, litres, time_to_fs, share_form = create_plan()
        return render_template('minimum_gas/min_gas.html', form=form , plan=plan, tank_form=tank_form, bar=bar, litres=litres, time_to_fs=time_to_fs, share_form = share_form)
    if (hash):
        sharedplan = ShareLink.query.filter_by(hash=hash).first_or_404()  
        depth = sharedplan.depth
        gas_switch = sharedplan.gas
        solve = sharedplan.solve
        plan, tank_form, bar, litres, time_to_fs, share_form = create_plan()
        flash('Share link generated. Click Users icon to copy.', 'info')
        return render_template('minimum_gas/min_gas.html', form=form , plan=plan, tank_form=tank_form, bar=bar, litres=litres, time_to_fs=time_to_fs, share_form = share_form, hash=hash)
    return render_template('minimum_gas/min_gas.html', form=form)


@minimum_gas_bp.route('/gas_used', methods=['POST'])
def gas_used():
    selected_tank =  int(request.form['tank'])
    litres = int(request.form['min_gas_L'])
    bar = min_gas_bar(litres, selected_tank)
    return {'bar':bar, 'selected_tank': selected_tank}

@socketio.on('shared_tank_change')
def shared_tank_change(data):
    print("Tank change event")
    selected_tank =  int(data['selected_tank'])
    litres = int(data['min_gas_l'])
    bar = min_gas_bar(litres, selected_tank)
    emit('shared_tank_change', ({'bar':bar, 'selected_tank': selected_tank}), to=data['room'])


@minimum_gas_bp.route('/share', methods=['POST'])
def share():
    depth = int(request.form['depth'])
    solve = int(request.form['solve'])
    gas = int(request.form['gas'])
    hash = get_hash()
    sharelink = ShareLink(depth = depth, gas = gas, solve = solve, hash = hash)
    db.session.add(sharelink)
    db.session.commit()
    return {'hash': hash}

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

def get_hash():
    import random
    import string
    import hashlib
    length = 6
    SIMPLE_CHARS = string.ascii_letters
    def get_random_string():
        return ''.join(random.choice(SIMPLE_CHARS) for i in range(length))
    hash = hashlib.sha256(str(get_random_string()).encode('utf-8'))
    return hash.hexdigest()[:length]
