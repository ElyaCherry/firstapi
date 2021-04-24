from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from items import Item, ItemList

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'


jwt = JWT(app, authenticate, identity)


# Endpoints
api.add_resource(Item, '/items/<name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
