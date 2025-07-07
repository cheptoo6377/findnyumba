from app import app
from app.extension import db
from app import models

def setup_initial_data():
    from app.models import RoleModel, UserModel
    from flask_security import hash_password
    import uuid

    roles_data = {
        'applicant': {
            'name': 'applicant',
            'description': 'Job applicant who can search and apply for jobs.'
        },
        'admin': {
            'name': 'admin',
            'description': 'Administrator with full access to manage jobs and users.'
        }
    }

    for role_data in roles_data.values():
        role = RoleModel.query.filter_by(name=role_data['name']).first()
        if not role:
            role = RoleModel(**role_data)
            db.session.add(role)
    db.session.commit()

    # Create admin user if not exists
    
      

 
with app.app_context():
    db.create_all()
    setup_initial_data()

if __name__ == "__main__":
    app.run(debug=True)