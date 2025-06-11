from flask_restful import Resource,marshal_with,fields,abort,reqparse
from app.models import ExchangeRequestModel
from app.extension import db

exchange_args = reqparse.RequestParser()
exchange_args.add_argument('requester_id', type=int, required=True, help='requester_id cannot be empty')
exchange_args.add_argument('property_id', type=int, required=True, help='property_id cannot be empty')
exchange_args.add_argument('message', type=str, required=False)
exchange_args.add_argument('status', type=str, required=False)
exchange_args.add_argument('created_at', type=str, required=False)

exchange_fields = {
     'id': fields.Integer,
    'requester_id': fields.Integer,
    'property_id': fields.Integer,
    'message': fields.String,
    'status': fields.String,
    'created_at': fields.String
}



class Exchange(Resource):
    @marshal_with(exchange_fields)
   
    def get(self):
      exchanges = ExchangeRequestModel.query.all()
      if not exchanges:
         abort(404,message='exchanges not found')
      return exchanges
    @marshal_with(exchange_fields)
    def post(self):
        args = exchange_args.parse_args()
        try:
            new_exchange = ExchangeRequestModel(
                requester_id=args['requester_id'],
                property_id=args['property_id'],
                message=args.get('message'),
                status=args.get('status', 'pending'),
                created_at=args.get('created_at')
            )
            db.session.add(new_exchange)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, message='error')
        exchanges = ExchangeRequestModel.query.all()
        return exchanges