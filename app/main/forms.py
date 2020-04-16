from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class DiveForm(FlaskForm):
    depth = IntegerField('Depth', validators=[Required()])
    solve = IntegerField('Solving time', validators=[Required()], default=1)
    gas = SelectField(u'Gas Switch', choices=[('21', '21m - 50%'), ('6', 'Oxygen'), ('0', 'Surface')])
    submit = SubmitField('Dive!')

class TankForm(FlaskForm):
    tank = SelectField(u'Tank', choices=[('14', 'D7'), ('17', 'D8.5'), ('20', 'D10'), ('24', 'D12'), ('30', 'D15')])
    min_gas_L = HiddenField()