# jobs.py
# This file can be used for job-related route logic or utilities.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import JobModel
from app.extension import db

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs')
def jobs_list():
    jobs = JobModel.query.all()
    return render_template('jobs.html', jobs=jobs)

# Add more job-related routes or logic here as needed.
