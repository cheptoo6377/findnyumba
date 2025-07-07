from flask import request
from flask_restful import Resource, marshal_with, fields, abort
from app.models import JobModel
from app.extension import db, csrf

# Output fields for marshalling responses
job_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'company': fields.String,
    'user_id': fields.Integer
}

# Resource to handle job list and creation
@csrf.exempt  # Exempt this resource from CSRF protection
class Jobs(Resource):

    @marshal_with(job_fields)
    def get(self):
        jobs = JobModel.query.all()
        if not jobs:
            abort(404, description='No jobs found')
        return jobs

    @marshal_with(job_fields)
    def post(self):
        data = request.get_json()

        # Validate required fields (user_id is not required from client)
        required_fields = ['title', 'description', 'company']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return {'message': 'Missing required fields', 'missing': missing}, 400

        # Optionally assign job to a user if user_id is provided (e.g., by employer)
        user_id = data.get('user_id')
        new_job = JobModel(
            title=data['title'],
            description=data['description'],
            company=data['company'],
            user_id=user_id if user_id else None
        )
        db.session.add(new_job)
        db.session.commit()
        return new_job, 201

# Resource to handle single job operations
@csrf.exempt  # Exempt this resource from CSRF protection
class Job(Resource):

    @marshal_with(job_fields)
    def get(self, id):
        job = JobModel.query.filter_by(id=id).first()
        if not job:
            abort(404, description='Job not found')
        return job

    def delete(self, id):
        job = JobModel.query.filter_by(id=id).first()
        if not job:
            abort(404, description='Job not found')

        db.session.delete(job)
        db.session.commit()
        return '', 204
