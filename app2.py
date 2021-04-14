from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

items = [
    {
        'name': 'default item name',
        'price': 1000
    }
]

parser = reqparse.RequestParser()


class Item(Resource):
    # GET /items/<name>
    def get(self, name):
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            return {'searched_item': item[0]}
        return {'message': 'item not found'}

    # POST /items/<name>
    def post(self, name):
        parser.add_argument('price')
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            return {'message': 'item already exists'}
        price = parser.parse_args()['price']
        if price.isdigit():
            items.append({'name': name, 'price': int(price)})
            return {'items': items}
        return {'message': 'price is not an integer'}

    # PUT /items/<name>
    def put(self, name):
        parser.add_argument('price')
        item = list(filter(lambda x: x['name'] == name, items))
        price = parser.parse_args()['price']
        if item:
            if price.isdigit():
                item[0]['price'] = int(price)
                return {'items': items}
            return {'message': 'price is not an integer'}
        Item.post(self, name)

    # DELETE /items/<name>
    def delete(self, name):
        item = list(filter(lambda x: x['name'] == name, items))
        if item:
            items.remove(item[0])
            return {'items': items}
        return {'message': 'item not found'}


api.add_resource(Item, '/items/<name>')


class ItemList(Resource):
    # GET /items
    def get(self):
        return {'items': items}

    # POST /items
    def post(self):
        parser.add_argument('itemlist', type=dict, action='append')
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


api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
