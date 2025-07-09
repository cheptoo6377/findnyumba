from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Optional

class CustomRegistrationForm(RegisterForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=20)])
