# Ensure user loader is set for Flask-Login

from flask import Flask, jsonify, request
from app.extension import db
from flask_restful import Api
from app.resources.user import Userr,Users
from app.resources.job import Job,Jobs
from app.models import RoleModel,UserModel,JobModel
from flask_security import SQLAlchemyUserDatastore,hash_password,verify_password, Security
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
import uuid
from app import routes  # Register all routes defined in app/routes.py
from app.routes import main as main_blueprint
from app.extension import csrf
from app.routes import mail
from app.forms.register import CustomRegistrationForm
from app.forms.login import CustomLoginForm
from config import Config
from app.resources.api_bp import api_bp







app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api=Api(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)
security = Security(app, user_datastore, register_form=CustomRegistrationForm, login_form=CustomLoginForm)
app.register_blueprint(main_blueprint)

csrf.init_app(app)
mail.init_app(app)

app.config['JWT_SECRET_KEY'] = 'your-very-strong-secret-key'  # Change this to a secure value
jwt = JWTManager(app)

# Exempt the API blueprint from CSRF protection
csrf.exempt(api_bp)

api.add_resource(Users, '/api/users')
api.add_resource(Userr, '/api/users/<int:id>')
api.add_resource(Jobs, '/api/jobs')
api.add_resource(Job, '/api/jobs/<int:id>')


# Example login route for JWT token generation

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
# Register the API blueprint (if not already registered)
app.register_blueprint(api_bp)

