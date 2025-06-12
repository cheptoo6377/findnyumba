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

app = Flask(__name__)

app.config['SECRET_KEY'] = '9c7122e76a4f0cdd13813494547ab17b00623d13d2e51016479f1f1e49e9d525'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config.from_object(Config)
db.init_app(app)
api=Api(app)



     
       
    
    
from app.forms import ExchangeForm
from flask import request


@app.route('/home')
def home():
    return "welcome"
    

@app.route('/property')
def property_page():
    return render_template('property.html')
@app.route('/exterior')
def exterior_page():
    return render_template('exterior.html')

@app.route('/interior')
def interior_page():
    return render_template('interior.html')

@app.route('/extra')
def extra_page():
    return render_template('extra.html')

@app.route('/exchange_form', methods=['GET', 'POST'])
def exchange_form():
    form = ExchangeForm()
    if form.validate_on_submit():
        # Process form data here (e.g., save to database)
        return render_template('forms.html', form=form, success=True)
    return render_template('forms.html', form=form)
    
  
  
  
        

api.add_resource(Users, '/api/users')
api.add_resource(Userr, '/api/users/<int:id>')
api.add_resource(Properties, '/api/properties')
api.add_resource(property, '/api/properties/<int:id>')
api.add_resource(Favoritez, '/api/favorites')
api.add_resource(Fav,'/api/favorites/<int:id>')
api.add_resource(Exchange,'/api/exchange')






    




