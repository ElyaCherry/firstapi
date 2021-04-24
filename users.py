from flask_restful import reqparse, abort, Resource
import sqlite3

parser = reqparse.RequestParser()


class User(object):
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        row = cur.execute(query, (username,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        row = cur.execute(query, (_id,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user


class UserRegister(Resource):
    @staticmethod
    def post():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        parser.add_argument('username', help="Username can't be blank")
        parser.add_argument('password', help="Password can't be blank")
        args = parser.parse_args()
        if list(cursor.execute("SELECT * FROM users WHERE username = '%s'" % args['username'])):
            abort(404, message="Username {} already exists.".format(args['username']))
        else:
            query = 'INSERT INTO users(id, username, password) VALUES (NULL, ?, ?)'
            user = (args['username'], args['password'])
            cursor.execute(query, user)
            connection.commit()
            connection.close()
            return "Successfully added user {}".format(args['username']), 201
