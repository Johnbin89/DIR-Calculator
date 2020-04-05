from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from ..import db
from .forms import DiveForm
from .diveplan import min_gas_plan


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
        #print(plan)
        return render_template('min_gas.html', form=form , plan=plan)
        print(2)
    return render_template('min_gas.html', form=form)

@main.route('/contactus')
def contactus():
    return render_template('contactus.html')