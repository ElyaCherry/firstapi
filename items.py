from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import reqparse, Resource
import sqlite3

# Query parser
parser = reqparse.RequestParser()
parser.add_argument('price', required=True)
parser.add_argument('items', type=dict, action="append", required=True)


# requested item doesn't exist error
def abort_if_item_doesnt_exist(name):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    if not list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)):
        abort(404, message="There's no such item in the shop ({})".format(name))
    connection.commit()
    connection.close()


# item already has been created
def abort_if_item_already_exists(name):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    if list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)):
        abort(404, message="You can't add this item, because it already exists ({})".format(name))
    connection.commit()
    connection.close()


# Class of items which allows to view, create, edit and delete one item
class Item(Resource):
    # GET /items/<name>
    # Get item by name
    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        abort_if_item_doesnt_exist(name)
        item = list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name))

        connection.commit()
        connection.close()

        return item, 201

    # POST /items/<name>
    # Create new item by name
    @jwt_required()
    def post(self, name):
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        abort_if_item_already_exists(name)
        args = parser.parse_args()
        query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
        item = (name, args['price'])
        cursor.execute(query, item)

        connection.commit()
        connection.close()

        return "Added items {}".format(item), 201

    # PUT /items/<name>
    # Edit price of an item by name
    # If no item found by name, create item by name
    @jwt_required()
    def put(self, name):
        args = parser.parse_args()
        item = (name, args['price'])

        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        if not list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)):
            query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
            cursor.execute(query, item)

            connection.commit()
            connection.close()
        else:
            query = "UPDATE items SET price = {0} WHERE name = '{1}'".format(args['price'], name)
            cursor.execute(query)

            connection.commit()
            connection.close()
        return item, 201

    # DELETE /items/<name>
    # Delete item by name
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        abort_if_item_doesnt_exist(name)
        query = "DELETE from items WHERE name = '%s'" % name
        cursor.execute(query)

        connection.commit()
        connection.close()

        return '', 204


class ItemList(Resource):
    # GET /items
    # Get a list of all items
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        item = list(cursor.execute("SELECT * FROM items"))

        connection.commit()
        connection.close()

        return item, 201

    # POST /items
    # Create several items
    # Takes dict with key 'items' and value list of item dicts
    @jwt_required()
    def post(self):
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        args = parser.parse_args()
        for i in range(len(args['items'])):
            abort_if_item_already_exists(args['items'][i]['name'])
            query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
            item = (args['items'][i]['name'], args['items'][i]['price'])
            cursor.execute(query, item)

        connection.commit()
        connection.close()
        return "Successfully added items {}".format(args['items']), 201

