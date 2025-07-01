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



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api=Api(app)


user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)
security = Security(app, user_datastore, register_form=CustomRegistrationForm)
app.register_blueprint(main_blueprint)

csrf.init_app(app)
mail.init_app(app)



api.add_resource(Users, '/api/users')
api.add_resource(Userr, '/api/users/<int:id>')
api.add_resource(Jobs, '/api/jobs')
api.add_resource(Job, '/api/jobs/<int:id>')