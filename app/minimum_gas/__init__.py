from flask import Blueprint

minimum_gas_bp = Blueprint('minimum_gas', __name__)

from app.minimum_gas import views