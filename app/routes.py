# User profile route (login required)


# Post-login redirect route for role-based dashboard
from app.forms.job_create import JobCreateForm

# Custom registration route for debugging
from app.extension import csrf

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import roles_required, login_user, current_user, logout_user
from app.models import JobModel, UserModel, RoleModel, JobApplication
from flask import session
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
        if current_user.has_role('admin'):
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.has_role('applicant'):
            return redirect(url_for('main.user_dashboard'))
    jobs = JobModel.query.all()
    return render_template('index.html', jobs=jobs)

@main.route('/admin/dashboard', endpoint='admin_dashboard')

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
    user = current_user
    user_jobs = JobModel.query.all()
    available_jobs = JobModel.query.all()
    return render_template('user_dashboard.html', user=user, user_jobs=user_jobs, available_jobs=available_jobs)

# Apply to job route

@main.route('/apply/<int:job_id>', methods=['POST'])
def apply_to_job(job_id):
   

    job = JobModel.query.get_or_404(job_id)

 

    new_application = JobApplication( job_id=job_id, user_id=UserModel.query.first().id)  # Assuming you want the first user for demonstration
    db.session.add(new_application)
    db.session.commit()
    flash('Application submitted successfully!', 'success')
    return render_template('your_jobs.html', job=job)
@main.route('/your-jobs')
def user_jobs():
    user_id = UserModel.query.all().first().id  # Assuming you want the first user for demonstration
   

    applications = JobApplication.query.filter_by(user_id=user_id).all()
    user_jobs = [app.job for app in applications]

    return render_template('your_jobs.html', user_jobs=user_jobs)


from flask import Blueprint, render_template
from app.models import JobModel



@main.route('/jobs', methods=['GET', 'POST'])

@csrf.exempt
def jobs():
    form = JobCreateForm()
    if form.validate_on_submit():
        new_job = JobModel(
            title=form.title.data,
            description=form.description.data,
            company=form.company.data,
        
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
    
    return redirect(url_for('main.admin_dashboard'))






