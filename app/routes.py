from flask_security import current_user, registerable, utils
from app.forms.register import CustomRegistrationForm
from app.forms.job_create import JobCreateForm

# Custom registration route for debugging

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import roles_required, login_user, current_user, logout_user
from app.models import JobModel, UserModel, RoleModel
# from app.forms.login import RegisterUserForm
from flask_security.utils import hash_password, verify_password
from app.extension import db
from flask_principal import Identity, identity_changed
from flask import current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import uuid

main = Blueprint('main', __name__)
mail = Mail()
serializer = URLSafeTimedSerializer('your-secret-key')


@main.route('/')
def index():
    if current_user.is_authenticated:
        # Only allow the predefined admin user (by email) to access admin dashboard
        if current_user.has_role('admin') and current_user.email == 'admin@example.com':
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.has_role('admin'):
            flash('You are not authorized as the system admin.', 'danger')
            logout_user()
            return redirect(url_for('security.login'))
        elif current_user.has_role('applicant'):
            return redirect(url_for('main.user_dashboard'))
    jobs = JobModel.query.all()
    return render_template('index.html', jobs=jobs)

@main.route('/admin/dashboard', endpoint='admin_dashboard')
@roles_required('admin')
def admin_dashboard():
    total_users = UserModel.query.count()
    total_jobs = JobModel.query.count()
    role_stats = {role.name: len(role.users.all()) for role in RoleModel.query.all()}
    recent_users = UserModel.query.order_by(UserModel.created_at.desc()).limit(5).all()
    jobs = JobModel.query.all()  # Pass all jobs to the template
    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_jobs=total_jobs,
        role_stats=role_stats,
        recent_users=recent_users,
        jobs=jobs
    )

@main.route('/user/dashboard')
def user_dashboard():
    user = UserModel.query.first()  # Example: get the first user
    user_jobs = JobModel.query.filter_by(user_id=user.id).all() if user else []
    return render_template('user_dashboard.html', user=user, user_jobs=user_jobs)
from flask import Blueprint, render_template
from app.models import JobModel



@main.route('/jobs', methods=['GET', 'POST'])
def jobs():
    form = JobCreateForm()
    if form.validate_on_submit():
        new_job = JobModel(
            title=form.title.data,
            description=form.description.data,
            company=form.company.data,
            user_id=form.user_id.data
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job created successfully!', 'success')
        return redirect(url_for('main.jobs'))
    jobs = JobModel.query.all()
    return render_template('jobs.html', jobs=jobs, form=form)

@main.route('/job/<int:id>/edit', methods=['GET', 'POST'])
def edit_job(id):
    job = JobModel.query.get_or_404(id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.location = request.form['location']
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('edit_job.html', job=job)

@main.route('/job/<int:id>/delete', methods=['POST'])
def delete_job(id):
    job = JobModel.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))


@main.route('/register', methods=['GET', 'POST'])
def custom_register():
    from app import user_datastore 
    form = CustomRegistrationForm()
    if form.validate_on_submit():
        # Assign default role 'applicant' on registration
        user = user_datastore.create_user(
            email=form.email.data,
            password=hash_password(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            active=True
        )
        applicant_role = user_datastore.find_role('applicant')
        if applicant_role:
            user_datastore.add_role_to_user(user, applicant_role)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('security.login'))
    else:
        if form.errors:
            print('Registration form errors:', form.errors)
    return render_template('security/register_user.html', register_user_form=form)
