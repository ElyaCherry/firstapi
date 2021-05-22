from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.items import ItemModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank!")

    # GET /items/<name>
    # Get item by name
    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item(name)
        if not item:
            return {'message': f"item '{name}' doesn't exist"}, 404
        return {'name': item.name, 'price': item.price}, 200

    # POST /items/<name>
    # Create new item by name
    @jwt_required()
    def post(self, name):
        if ItemModel.get_item(name):
            return {'message': f"item '{name}' already exists"}, 400
        price = ItemResource.parser.parse_args()['price']
        item = ItemModel(name=name, price=price)
        item.add_item()
        return {'name': name, 'price': price}, 201

    # PUT /items/<name>
    # Edit price of an item by name
    # If no item found by name, create item by name
    @jwt_required()
    def put(self, name):
        price = ItemResource.parser.parse_args()['price']
        if not ItemModel.get_item(name):
            item = ItemModel(name=name, price=price)
            item.add_item()
            return {'name': name, 'price': price}, 201
        ItemModel.change_item(name, price)
        return {'name': name, 'price': price}, 200

    # DELETE /items/<name>
    # Delete item by name
    @jwt_required()
    def delete(self, name):
        item = ItemModel.get_item(name)
        if not item:
            return {'message': f"item '{name}' doesn't exist"}, 404
        item.delete_item()
        return {}, 204


class ItemListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, required=True, action='append', help='This field cannot be blank!')

    # GET /items
    # Get a list of all items
    @jwt_required()
    def get(self):
        items = ItemModel.get_items()
        return {'items': [{'name': item.name, 'price': item.price} for item in items]}

    # POST /items
    # Create several items
    @jwt_required()
    def post(self):
        items = ItemListResource.parser.parse_args()['items']
        bad_item_names = []
        for item in items:
            existing_item = ItemModel.get_item(item['name'])
            if existing_item:
                bad_item_names.append(existing_item.name)
        if bad_item_names:
            return {'message': f"items '{bad_item_names}' already exist"}, 400

        for item in items:
            new_item = ItemModel(name=item.name, price=item['price'])
            new_item.add_item()
        return {'items': items}, 201

    @jwt_required()
    def delete(self):
        if not ItemModel.get_items():
            return {'message': f"There are no items in the store"}, 400
        ItemModel.delete_items()
        return {}, 204

