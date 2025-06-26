from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import roles_required, login_user, current_user
from app.models import JobModel, UserModel, RoleModel
from app.login import RegisterUserForm
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
    jobs = JobModel.query.all()  # Pass all jobs to the template
    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_jobs=total_jobs,
        role_stats=role_stats,
        recent_users=recent_users,
        jobs=jobs
    )

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = UserModel(
            email=form.email.data,
            password=hash_password(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register_user.html', form=form)
# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = UserModel.query.filter_by(email=email).first()
#         if user and verify_password(password, user.password):
#             login_user(user)
#             # Set up Flask-Principal identity
#             identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
#             flash('Logged in successfully.', 'success')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Invalid email or password.', 'danger')
#     return render_template('login_user.html')

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

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            msg = Message('Password Reset Request',
                          sender='noreply@findjob.com',
                          recipients=[email])
            reset_url = url_for('main.reset_password', token=token, _external=True)
            msg.body = f"Hello,\n\nTo reset your password, visit the following link:\n{reset_url}\n\nIf you did not request this, please ignore this email."
            mail.send(msg)
        flash('If this email exists in our system, a password reset link will be sent.', 'info')
        return redirect(url_for('main.login'))
    return render_template('forgot_password.html')

@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour expiry
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('main.forgot_password'))
    except BadSignature:
        flash('Invalid or tampered password reset link.', 'danger')
        return redirect(url_for('main.forgot_password'))
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        flash('Invalid user.', 'danger')
        return redirect(url_for('main.forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html', token=token)
        user.password = hash_password(password)
        db.session.commit()
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_password.html', token=token)
