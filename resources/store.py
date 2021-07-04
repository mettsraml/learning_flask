from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )


    @jwt_required()
    def get(self, name):            
        item = StoreModel.find_by_name(name)
        
        if item:
            return item.json()
        return {'message': 'Store not found'}, 404

    
    def post(self, name):
        
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exitst".format(name)}, 400
        
        # data = Item.parser.parse_args()
        store = StoreModel(name)
        
        try:
            StoreModel.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}, 500

        return store.json(), 201
    
    @jwt_required()
    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Store deleted'}
    
    
    
    
class StoreList(Resource):
    def get(self):
        return {'items': [item.json() for item in StoreModel.query.all()]}