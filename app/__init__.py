from flask import Flask,render_template

from app.extension import db

from config import Config
from flask_security import SQLAlchemyUserDatastore,hash_password
from flask_security.signals import user_registered
from flask_restful import Api
from app.resources.user import Userr,Users
from app.resources.property import Properties,property
from app.resources.favorite import Favoritez,Fav
from app.resources.exchange import Exchange
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9c7122e76a4f0cdd13813494547ab17b00623d13d2e51016479f1f1e49e9d525'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
    app.config.from_object(Config)
    db.init_app(app)
    api=Api(app)



     
       
    
    

   

    
  
  
  
        

    api.add_resource(Users, '/api/users')
    api.add_resource(Userr, '/api/users/<int:id>')
    api.add_resource(Properties, '/api/properties')
    api.add_resource(property, '/api/properties/<int:id>')
    api.add_resource(Favoritez, '/api/favorites')
    api.add_resource(Fav,'/api/favorites/<int:id>')
    api.add_resource(Exchange,'/api/exchange')
    





    return app




