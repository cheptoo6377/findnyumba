from flask import Flask
from app.extension import db
from flask_restful import Api
from app.resources.user import Userr,Users
from app.resources.job import Job,Jobs
from app.models import RoleModel,UserModel
from flask_security import SQLAlchemyUserDatastore,hash_password
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '39363b388a36272b39b2dbee268ff803'  
app.config['SECURITY_PASSWORD_SINGLE_HASH'] = True 
db.init_app(app)
api=Api(app)










api.add_resource(Users, '/api/users')
api.add_resource(Userr, '/api/users/<int:id>')
api.add_resource(Jobs, '/api/jobs')
api.add_resource(Job, '/api/jobs/<int:id>')