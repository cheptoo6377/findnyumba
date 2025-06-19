from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import roles_required, login_user, current_user
from app.models import JobModel, UserModel, RoleModel
from app.login import RegisterUserForm
from flask_security.utils import hash_password, verify_password
from app.extension import db
from flask_principal import Identity, identity_changed
from flask import current_app
import uuid

main = Blueprint('main', __name__)

@main.route('/')
def root():
    return "Welcome to the House Search API!", 200

@main.route('/home')
def index():
    if current_user.is_authenticated:
        if current_user.has_role('admin'):
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.has_role('user'):
            return redirect(url_for('main.user_dashboard'))
    jobs = JobModel.query.all()
    return render_template('index.html', jobs=jobs)

@main.route('/admin/dashboard', endpoint='admin_dashboard')
# @roles_required('admin')
def admin_dashboard():
    total_users = UserModel.query.count()
    total_jobs = JobModel.query.count()
    role_stats = {role.name: len(role.users.all()) for role in RoleModel.query.all()}
    recent_users = UserModel.query.order_by(UserModel.created_at.desc()).limit(5).all()
    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_jobs=total_jobs,
        role_stats=role_stats,
        recent_users=recent_users
    )

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        if UserModel.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.register'))
        user = UserModel(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            password=hash_password(form.password.data),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register_user.html', register_user_form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserModel.query.filter_by(email=email).first()
        if user and verify_password(password, user.password):
            login_user(user)
            # Set up Flask-Principal identity
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@main.route('/user/dashboard')
def user_dashboard():
    user = UserModel.query.first()  # Example: get the first user
    user_jobs = JobModel.query.filter_by(user_id=user.id).all() if user else []
    return render_template('user_dashboard.html', user=user, user_jobs=user_jobs)
from flask import Blueprint, render_template
from app.models import JobModel



@main.route('/jobs')
def jobs():
    jobs = JobModel.query.all()
    return render_template('jobs.html', jobs=jobs)

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
