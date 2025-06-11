
from flask_restful import Resource,marshal_with,fields,abort,reqparse
from app.models import PropertyModel
from app.extension import db

property_args = reqparse.RequestParser()
property_args.add_argument('price', type=int, required=True, help='price cannot be empty')
property_args.add_argument('location', type=str, required=True, help='location cannot be empty')
property_args.add_argument('type', type=str, required=True, help='type cannot be empty')
property_args.add_argument('image_url', type=str, required=False)
property_args.add_argument('date_listed', type=str, required=False)
property_args.add_argument('status', type=str, required=False)




property_fields = {
    'id': fields.Integer,
    'price': fields.Integer,
    'location': fields.String,
    'type': fields.String,
    'image_url': fields.String,
    'date_listed': fields.String,
    'status': fields.String
}

class Properties(Resource):
   @marshal_with(property_fields)
   
   def get(self):
      properties = PropertyModel.query.all()
      if not properties:
         abort(404,message='properties not found')
      return properties
   @marshal_with(property_fields)
   def post(self):
      args = property_args.parse_args()
      try:
         new_property = PropertyModel(
            price=args['price'],
            location=args['location'],
            type=args['type'],
            image_url=args.get('image_url'),
            date_listed=args.get('date_listed'),
            status=args.get('status', 'available')
         )
         db.session.add(new_property)
         db.session.commit()
      except Exception as e:
         db.session.rollback()
         abort(400, message='error')
      properties = PropertyModel.query.all()
      return properties
   
class property(Resource):
   @marshal_with(property)
   def get(self,id):
      proper = PropertyModel.query.filter_by(id=id).first()
      
      if not proper:
         abort(404,message='property not found')
      return proper
   
   @marshal_with(property_fields)
   def patch(self, id):
      args = property_args.parse_args()
      prop = PropertyModel.query.filter_by(id=id).first()
      if not prop:
         abort(404, message="Property with that id not found")
      if args["price"] is not None:
         prop.price = args["price"]
      if args["location"] is not None:
         prop.location = args["location"]
      if args["type"] is not None:
         prop.type = args["type"]
      if args["image_url"] is not None:
         prop.image_url = args["image_url"]
      if args["date_listed"] is not None:
         prop.date_listed = args["date_listed"]
      if args["status"] is not None:
         prop.status = args["status"]
      db.session.commit()
      return prop
   @marshal_with(property_fields)
   def delete(self, id):
      prop = PropertyModel.query.filter_by(id=id).first()
      if not prop:
         abort(404, message="Property with that id not found")
      db.session.delete(prop)
      db.session.commit()
      return prop
   
  