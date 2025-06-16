from flask import render_template, request,Flask,redirect,url_for,flash
from flask_security import roles_required,login_user
from app.models import JobModel
from app.login import RegisterUserForm
from flask_security.utils import hash_password, verify_password
from app.extension import db
import uuid

app = Flask(__name__)
@app.route('/home')
def index():
    jobs = JobModel.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = JobModel.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

from app.models import JobModel, UserModel, RoleModel


@app.route('/admin/dashboard')
@roles_required
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        if UserModel.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
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
        return redirect(url_for('login'))
    return render_template('register_user.html', register_user_form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserModel.query.filter_by(email=email).first()
        if user and verify_password(password, user.password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')