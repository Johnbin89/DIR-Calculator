from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from ..import db
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@main.route('/minimum-gas')
def minimum_gas():
    return render_template('min_gas.html')

@main.route('/contactus')
def contactus():
    return render_template('contactus.html')