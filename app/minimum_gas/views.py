from flask import flash, render_template, request

from app import db
from app.minimum_gas import minimum_gas_bp
from app.minimum_gas.forms import DiveForm, ShareForm, TankForm
from app.models import ShareLink, generate_share_hash
from app.planning.diveplan import calculate_plan, min_gas_bar
from app.planning.validation import (
    plan_warning,
    read_int,
    read_tank,
    validate_plan_input,
)


@minimum_gas_bp.route('/minimum-gas', methods=['GET', 'POST'])
@minimum_gas_bp.route('/minimum-gas/<hash>')
def minimum_gas(hash=None):
    form = DiveForm()
    if form.validate_on_submit():
        depth = form.depth.data
        gas_switch = int(form.gas.data)
        warning = plan_warning(depth, gas_switch)
        if warning:
            flash(warning)
            return render_template('minimum_gas/min_gas.html', form=form)
        solve = form.solve.data
        #print(depth, gas_switch)
        plan, tank_form, bar, litres, time_to_fs, share_form = create_plan(depth, gas_switch, solve)
        return render_template('minimum_gas/min_gas.html', form=form , plan=plan, tank_form=tank_form, bar=bar, litres=litres, time_to_fs=time_to_fs, share_form = share_form)
    if (hash):
        sharedplan = ShareLink.query.filter_by(hash=hash).first_or_404()
        #sharedplan = db.session.scalars(db.select(ShareLink).filter_by(hash=hash)).first() #SQLAlchemy 2.0 
        depth = sharedplan.depth
        gas_switch = sharedplan.gas
        solve = sharedplan.solve
        plan, tank_form, bar, litres, time_to_fs, share_form = create_plan(depth, gas_switch, solve, sharedplan.tank)
        form.depth.data = depth
        form.gas.data = gas_switch
        form.solve.data = solve
        flash('Share link generated. Click Users icon to copy.', 'info')
        return render_template('minimum_gas/min_gas.html', form=form, depth=depth, gas_switch=gas_switch, solve=solve , plan=plan, tank_form=tank_form, bar=bar, litres=litres, time_to_fs=time_to_fs, share_form = share_form, hash=hash)
    return render_template('minimum_gas/min_gas.html', form=form)


#@minimum_gas_bp.route('/gas_used', methods=['POST'])
@minimum_gas_bp.post('/gas_used') #bp.post (e.g get,put,post)added in Flask 2.0
def gas_used():
    errors = {}
    selected_tank = read_tank(request.form, 'tank', errors)
    litres = read_int(request.form, 'min_gas_L', errors)
    if errors:
        return {'errors': errors}, 422
    bar = min_gas_bar(litres, selected_tank)
    return {'bar':bar, 'selected_tank': selected_tank}


@minimum_gas_bp.route('/share', methods=['POST'])
def share():
    depth, solve, gas, tank, errors = validate_plan_input(request.form)
    if errors:
        return {'errors': errors}, 422
    warning = plan_warning(depth, gas)
    if warning:
        return {'warning': warning}, 422
    hash = generate_share_hash()
    sharelink = ShareLink(depth = depth, gas = gas, solve = solve, tank = tank, hash = hash)
    db.session.add(sharelink)
    db.session.commit()
    return {'hash': hash}


def create_plan(depth, gas_switch, solve, tank=24):
    plan, bar, litres, time_to_fs = calculate_plan(depth, gas_switch, solve, tank)
    tank_form = TankForm(tank=tank, min_gas_L = litres)
    share_form = ShareForm(depth = depth, solve = solve, gas_switch = gas_switch)
    return plan,tank_form, bar, litres, time_to_fs, share_form