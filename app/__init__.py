# Ensure user loader is set for Flask-Login

from flask import Flask, jsonify, request
from app.extension import db
from flask_restful import Api
from app.resources.user import Userr,Users
from app.resources.job import Job,Jobs
from app.models import RoleModel,UserModel,JobModel
from flask_security import SQLAlchemyUserDatastore,hash_password,verify_password, Security

import uuid
from app import routes  # Register all routes defined in app/routes.py
from app.routes import main as main_blueprint
from app.extension import csrf
from app.routes import mail
from app.forms.register import CustomRegistrationForm

from config import Config

from flask_wtf.csrf import CSRFProtect






csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api=Api(app)

# Initialize Flask-Login



user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)

security = Security(app, user_datastore, register_form=CustomRegistrationForm, )
# Initialize Flask-Security with custom user datastore and registration form
 # Create database tables

app.register_blueprint(main_blueprint)

csrf.init_app(app)

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'your_key'


mail.init_app(app)

from flask_security.signals import user_registered

@user_registered.connect_via(app)
def user_registered_sighandler(sender, user, confirm_token, **extra):
        """Handle post-registration logic"""
        # Assign default 'Applicant' role
        default_role = RoleModel.query.filter_by(name='applicant').first()
        if default_role and not user.roles:
            user.roles.append(default_role)
            db.session.commit()

        print(f"New user registered: {user.email} with roles: {[role.name for role in user.roles]}")



# Change this to a secure value


# Exempt the API blueprint from CSRF protection


api.add_resource(Users, '/api/users')
api.add_resource(Userr, '/api/users/<int:id>')
api.add_resource(Jobs, '/api/jobs')
api.add_resource(Job, '/api/jobs/<int:id>')


# Example login route for JWT token generation

from flask_wtf.csrf import CSRFError
from flask import render_template






