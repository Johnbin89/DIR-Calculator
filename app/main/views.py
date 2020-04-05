from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from ..import db
from .forms import DiveForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/minimum-gas')
def minimum_gas():
    form = DiveForm()
    return render_template('min_gas.html', form=form)

@main.route('/contactus')
def contactus():
    return render_template('contactus.html')