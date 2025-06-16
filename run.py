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

    # Create admin user
    admin_role = RoleModel.query.filter_by(name='admin').first()
    admin_user = UserModel.query.filter_by(email='cheptoodorothy69@example.com').first()
    if not admin_user:
        admin_user = UserModel(
            email='cheptoodorothy69@example.com',
            first_name='deom',
            last_name='cysry',
            password=('@Cheptoo6377'),
            active=True,
            roles=[admin_role],
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email:", admin_user.email)

    # Create applicant user
    applicant_role = RoleModel.query.filter_by(name='applicant').first()
    applicant_user = UserModel.query.filter_by(email='applicant@example.com').first()
    if not applicant_user:
        applicant_user = UserModel(
            email='applicant@example.com',
            first_name='Jane',
            last_name='Doe',
            password=('12345'),
            active=True,
            roles=[applicant_role],
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(applicant_user)
        db.session.commit()
        print("Applicant user created with email:", applicant_user.email)

with app.app_context():
    db.create_all()
    setup_initial_data()

if __name__ == "__main__":
    app.run(debug=True)