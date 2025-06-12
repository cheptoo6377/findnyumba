from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class ExchangeForm(FlaskForm):
    requester_id = IntegerField('Requester ID', validators=[DataRequired()])
    property_id = IntegerField('Property ID', validators=[DataRequired()])
    message = StringField('Message', validators=[Optional()])
    status = StringField('Status', validators=[Optional()])
    created_at = StringField('Created At', validators=[Optional()])
    submit = SubmitField('Submit')