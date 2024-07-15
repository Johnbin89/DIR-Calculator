from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import InputRequired, ValidationError

def check_positive(form, field):
    if field.data <= 0:
        raise ValidationError('Provide positive integer')

def solve_time_1(form, field):
    if field.data < 1:
        raise ValidationError("Less than a minute to handle Out-Of-Gas?")
    
class DiveForm(FlaskForm):
    depth = IntegerField('Depth', validators=[InputRequired(), check_positive])
    solve = IntegerField('Solving time', validators=[InputRequired(), solve_time_1], default=1)
    gas = SelectField(u'Gas Switch', choices=[('21', '21m - 50%'), ('6', 'Oxygen'), ('0', 'Surface')])
    submit = SubmitField('Dive!')

class TankForm(FlaskForm):
    tank = SelectField(u'Tank', choices=[('14', 'D7'), ('17', 'D8.5'), ('20', 'D10'), ('24', 'D12'), ('30', 'D15')], id='selected_tank')
    min_gas_L = HiddenField(id='min_gas_l')

class ShareForm(FlaskForm):
    depth = HiddenField()
    solve = HiddenField()
    gas = HiddenField()