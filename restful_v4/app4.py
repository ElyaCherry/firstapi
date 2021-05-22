from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.items import ItemResource, ItemListResource
from resources.users import UserRegisterResource
from db import db

app = Flask(__name__)
api = Api(app)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

# Endpoints
api.add_resource(ItemResource, '/items/<string:name>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserRegisterResource, '/register')

if __name__ == '__main__':
    app.run(debug=True)
