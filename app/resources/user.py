
from flask_restful import Resource,marshal_with,fields,abort,reqparse
from app.models import UserModel
from app.extension import db



#DATABASE MODEL

   
#request parser
user_args = reqparse.RequestParser()

user_args.add_argument('email', type=str, required=True, help='email cannot be empty')
user_args.add_argument('password', type=str, required=True, help='password cannot be empty')
user_args.add_argument('first_name', type=str, required=False)
user_args.add_argument('last_name', type=str, required=False)
user_args.add_argument('phone_number', type=str, required=False)
user_args.add_argument('active', type=bool, required=False)


#output fields
user_fields = {
   'id': fields.Integer,
 
   'email': fields.String,
   'password' : fields.String,
    'first_name': fields.String,
   'last_name': fields.String,
   'phone_number': fields.String,
   'active': fields.Boolean
}

#resource for all users
class Users(Resource):
   @marshal_with(user_fields)
   #get all users
   def get(self):
      users = UserModel.query.all()
      if not users:
         abort(404,message='users not found')
      return users
   

   @marshal_with(user_fields)
   #create a user
   def post(self):
      args = user_args.parse_args()
      try:
         new_user = UserModel(
                               email=args['email'] , 
                               password=args['password'],
                               first_name=args.get('first_name'),
                               last_name=args.get('last_name'),
                                phone_number=args.get('phone_number'),
                                active=args.get('active', True))
         db.session.add(new_user)
         db.session.commit()
          
      except Exception as e:
         db.session.rollback()
         abort(400, message='error')
      users = UserModel.query.all()
      return users
        
      
         
   
class Userr(Resource):
   @marshal_with(user_fields)
   def get(self,id):
      user = UserModel.query.filter_by(id=id).first()
      
      if not user:
         abort(404,message='user not found')
      return user
   

  
   
   @marshal_with(user_fields)
   def patch(self, id):
         args = user_args.parse_args()
         user = UserModel.query.filter_by(id=id).first()
         if not user:
            abort(404, message="User with that id not found")
        
         user.email = args["email"]
         user.password = args["password"]
         user.first_name = args["first_name"]
         user.last_name = args["last_name"]
         user.phone_number = args["phone_number"]
         user.active = args["active"]
         db.session.commit()
         return user 
   @marshal_with(user_fields)
   def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
           abort(404,message="cannot delete this user")
        db.session.delete(user)
        db.session.commit()
        
      

   