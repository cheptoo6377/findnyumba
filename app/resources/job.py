
from flask_restful import Resource,marshal_with,fields,abort,reqparse
from app.models import JobModel
from app.extension import db



#DATABASE MODEL

   
#request parser
job_args = reqparse.RequestParser()

job_args.add_argument('title', type=str, required=True, help='Title of the job is required')
job_args.add_argument('description', type=str, required=True, help='Description is required')
job_args.add_argument('company', type=str, required=True, help='Company name is required')
job_args.add_argument('user_id', type=int, required=True, help='User ID is required')

job_fields={

    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'company': fields.String,
    'user_id': fields.Integer
}
class Jobs(Resource):
   @marshal_with(job_fields)
   #get all jobs
   def get(self):
      jobs = JobModel.query.all()
      if not jobs:
         abort(404,message='users not found')
      return jobs
   @marshal_with(job_fields)
   def post(self):
      args = job_args.parse_args()
      new_job = JobModel(
         title=args['title'],
         description=args['description'],
         company=args['company'],
         user_id=args['user_id']
      )
      db.session.add(new_job)
      db.session.commit()
      return new_job, 201
class Job(Resource):
    @marshal_with(job_fields)
    def get(self,id):
      job = JobModel.query.filter_by(id=id).first()
      
      if not job:
         abort(404,message='user not found')
      return job
    
    def delete(self, id):
        job = JobModel.query.filter_by(id=id).first()
        if not job:
            abort(404, message='job not found')
        db.session.delete(job)
        db.session.commit()
        return {'message': 'Job deleted successfully'}, 204
   