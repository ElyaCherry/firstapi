from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import reqparse, Resource



# Query parser
parser = reqparse.RequestParser()


# Class of items which allows to view, create, edit and delete one item
class Item(Resource):
    # GET /items/<name>
    # Get item by name
    @jwt_required()
    def get(self, name):
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            return {'searched_item': item[0]}
        return {'message': 'item not found'}

    # POST /items/<name>
    # Create new item by name
    @jwt_required()
    def post(self, name):
        parser.add_argument('price', required=True)
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            return {'message': 'item already exists'}
        price = parser.parse_args()['price']
        if price.isdigit():
            items.append({'name': name, 'price': int(price)})
            return {'items': items}
        return {'message': 'price is not an integer'}

    # PUT /items/<name>
    # Edit price of an item by name
    # If no item found by name, create item by name
    @jwt_required()
    def put(self, name):
        parser.add_argument('price', required=True)
        item = list(filter(lambda x: x['name'] == name, items))
        price = parser.parse_args()['price']
        if item:
            if price.isdigit():
                item[0]['price'] = int(price)
                return {'items': items}
            return {'message': 'price is not an integer'}
        Item.post(self, name)

    # DELETE /items/<name>
    # Delete item by name
    @jwt_required()
    def delete(self, name):
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            items.remove(item[0])
            return {'items': items}
        return {'message': 'item not found'}


class ItemList(Resource):
    # GET /items
    # Get a list of all items
    @jwt_required()
    def get(self):
        return {'items': items}

    # POST /items
    # Create several items
    # Takes dict with key 'items' and value list of item dicts
    @jwt_required()
    def post(self):
        parser.add_argument('itemlist', type=dict, action='append', required=True)
        itemlist = parser.parse_args()['itemlist']
        messages = []
        for item in itemlist:
            if list(filter(lambda x: x['name'] == item['name'], items)):
                messages.append({'name': item['name'], 'message': 'failed to create an item: item already exists'})
            else:
                if isinstance(item['price'], int):
                    items.append({'name': item['name'], 'price': item['price']})
                    messages.append({'name': item['name'], 'message': 'item successfully created'})
                messages.append({'name': item['name'], 'message': 'failed to create an item: price is not an integer'})
        return {'messages': messages, 'items': items}

