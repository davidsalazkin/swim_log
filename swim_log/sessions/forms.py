from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional


class LogSwim(FlaskForm):
    session_date = DateField('Date')
    swim_type = SelectField('Type', choices=[('Working', 'Working'), ('Warm-Up', 'Warm-Up'), ('Speed', 'Speed'), ('Distance', 'Distance')], default='Working')
    swim_stroke = SelectField('Stroke', choices=[('Freestyle', 'Freestyle'), ('Backstroke', 'Backstroke'), ('Breaststroke', 'Breaststroke'), ('Butterfly', 'Butterfly')], default='Freestyle')
    swim_distance = IntegerField('Distance (in yards)', validators=[DataRequired()])
    swim_time = IntegerField('Time (in seconds)', validators=[Optional()])
    submit = SubmitField('Submit Swim')
