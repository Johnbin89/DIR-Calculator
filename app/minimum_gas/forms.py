from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SelectChoice, SelectField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from app.planning.validation import GAS_SWITCHES, TANKS


def as_choices(options):
    return [SelectChoice(str(value), label) for value, label in options.items()]


def check_positive(form, field):
    if field.data <= 0:
        raise ValidationError("Provide positive integer")


def solve_time_1(form, field):
    if field.data < 1:
        raise ValidationError("Less than a minute to handle Out-Of-Gas?")


class DiveForm(FlaskForm):
    depth = IntegerField("Depth", validators=[InputRequired(), check_positive])
    solve = IntegerField(
        "Solving time", validators=[InputRequired(), solve_time_1], default=1
    )
    gas = SelectField("Gas Switch", choices=as_choices(GAS_SWITCHES))
    submit = SubmitField("Dive!")


class TankForm(FlaskForm):
    # autocomplete off: browsers otherwise restore the old option on refresh, next
    # to the pressure the server calculated for the saved tank
    tank = SelectField(
        "Tank",
        choices=as_choices(TANKS),
        id="selected_tank",
        render_kw={"autocomplete": "off"},
    )
    min_gas_L = HiddenField(id="min_gas_l")


class ShareForm(FlaskForm):
    depth = HiddenField()
    solve = HiddenField()
    gas = HiddenField()
