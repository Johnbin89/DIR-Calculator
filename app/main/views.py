from flask import render_template, session, redirect, url_for, flash, current_app, request, json
from . import main
from ..import db
from .forms import DiveForm, TankForm
from .diveplan import min_gas_plan, min_gas_litres, min_gas_bar


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/minimum-gas', methods=['GET', 'POST'])
def minimum_gas():
    form = DiveForm()  
    if form.validate_on_submit():
        depth = form.depth.data
        gas_switch = int(form.gas.data)
        if gas_switch == 0 and depth > 30:
            flash('Better take a stage, if you want to go below 30 meters.')
            return render_template('min_gas.html', form=form)
        solve = form.solve.data
        #print(depth, gas_switch)
        plan = min_gas_plan(depth, gas_switch, solve)
        time_to_fs = plan[1][1] - solve   #time need from depth to first stop
        print(plan)
        litres = min_gas_litres(plan)
        bar = min_gas_bar(litres, 24)
        tank_form = TankForm(tank=24, min_gas_L = litres)
        return render_template('min_gas.html', form=form , plan=plan, tank_form=tank_form, bar=bar, litres=litres, time_to_fs=time_to_fs)
    return render_template('min_gas.html', form=form)


@main.route('/gas_used', methods=['POST'])
def gas_used():
    selected_tank =  int(request.form['tank'])
    litres = int(request.form['min_gas_L'])
    bar = min_gas_bar(litres, selected_tank)
    return json.dumps({'bar':bar})
