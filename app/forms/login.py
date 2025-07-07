from flask_security import LoginForm
from wtforms import SelectField

class CustomLoginForm(LoginForm):
    role = SelectField( choices=[('admin', 'Admin'), ('applicant', 'Applicant')])
