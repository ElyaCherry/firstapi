from models.users import UserModel
from flask_restful import reqparse, Resource


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank and it must exist!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank and it must exist!"
    )

    def post(self):
        user = UserRegister.parser.parse_args()
        if UserModel.find_by_username(user['username']):
            return {'message': f"user {user['username']} already exists"}, 400
        user = UserModel(**user)
        user.add_user()
        return user.json(), 201
