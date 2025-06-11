
from flask_restful import Resource,marshal_with,fields,abort,reqparse
from app.models import FavoriteModel
from app.extension import db

favorite_args = reqparse.RequestParser()
favorite_args.add_argument('user_id', type=int, required=True, help='user_id cannot be empty')
favorite_args.add_argument('property_id', type=int, required=True, help='property_id cannot be empty')
favorite_args.add_argument('created_at', type=str, required=False)

favorite_fields ={
   'id': fields.Integer,
    'user_id': fields.Integer,
    'property_id': fields.Integer,
    'created_at': fields.String

}

class Favoritez(Resource):
    @marshal_with(favorite_fields)
   
    def get(self):
      favorites = FavoriteModel.query.all()
      if not favorites:
         abort(404,message='favorites not found')
      return favorites
    @marshal_with(favorite_fields)
    def post(self):
        args = favorite_args.parse_args()
        try:
            new_favorite = FavoriteModel(
                user_id=args['user_id'],
                property_id=args['property_id'],
                created_at=args.get('created_at')
            )
            db.session.add(new_favorite)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, message='error')
        favorites = FavoriteModel.query.all()
        return favorites
    
class Fav(Resource):
    @marshal_with(favorite_fields)
    def get(self, id):
        favorite = FavoriteModel.query.filter_by(id=id).first()
        if not favorite:
            abort(404, message='favorite not found')
        return favorite
    @marshal_with(favorite_fields)
    def delete(self, id):
        favorite = FavoriteModel.query.filter_by(id=id).first()
        if not favorite:
            abort(404, message='favorite not found')
        db.session.delete(favorite)
        db.session.commit()
        return favorite
