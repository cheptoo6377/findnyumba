from app.extension import db
from flask_security import UserMixin,RoleMixin
import uuid

#association table
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )

class UserModel(db.Model,UserMixin):
    __tablename__ = 'users'
    #basic identity fields that comes with flask security
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    #profile
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True, nullable=True)


    #account status
    active = db.Column(db.Boolean(),default=True)
   
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
 



    #roles
    roles = db.relationship('RoleModel', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return f"<User {self.email} {self.roles}>"
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email.split('@')[0] #fallback if no first name or last name
   
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles) 
    

    
    

class RoleModel(db.Model,RoleMixin):
    __tablename__ = 'roles'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'
    
class PropertyModel(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    date_listed = db.Column(db.Date, nullable=False, default=db.func.current_date())
    status = db.Column(db.String(50), nullable=False, default='available')  # e.g. available, sold, pending

    def __repr__(self):
        return f"<Property {self.type} - {self.location} - {self.status}>"




class ExchangeRequestModel(db.Model):
    __tablename__ = 'exchange_requests'
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # e.g. pending, accepted, rejected
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    requester = db.relationship('UserModel', backref=db.backref('exchange_requests', lazy='dynamic'))
    property = db.relationship('PropertyModel', backref=db.backref('exchange_requests', lazy='dynamic'))

    def __repr__(self):
        return f"<ExchangeRequest {self.id} - {self.status}>"
    


class FavoriteModel(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('UserModel', backref=db.backref('favorites', lazy='dynamic'))
    property = db.relationship('PropertyModel', backref=db.backref('favorites', lazy='dynamic'))

    def __repr__(self):
        return f"<Favorite User:{self.user_id} Property:{self.property_id}>"

    
