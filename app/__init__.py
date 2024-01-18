from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
from config import config


db = SQLAlchemy()
#mysql = MySQL()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    #mysql.init_app(app)

    #attach routes and custom error pages here
    from app.main import main as main_blueprint
    from app.errors import errors_bp as errors_blueprint
    from app.minimum_gas import minimum_gas_bp as min_gas_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(min_gas_blueprint)

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app    