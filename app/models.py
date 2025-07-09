from flask_sqlalchemy import SQLAlchemy
from app.extension import db
from flask_security import UserMixin



#association table
roles_users = db.Table('roles_user',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )



class JobModel(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    company = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'

class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    #basic identity fields that comes with flask security
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    #profile
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True, nullable=True)

    #account status
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    applications = db.relationship('JobApplication', backref='user', lazy=True)


    # roles relationship
    roles = db.relationship('RoleModel', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    jobs = db.relationship('JobModel', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email} {self.roles}>"
    def is_active(self):
        return self.active

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email.split('@')[0]  # fallback if no first name or last name

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def verify_and_update_password(self, password):
        from flask_security.utils import verify_password
        return verify_password(password, self.password)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

class RoleModel(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}>'

    def get_permissions(self):
        return []
    
class JobApplication(db.Model):
    __tablename__ = 'job_application'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    job = db.relationship('JobModel', backref='applications')
