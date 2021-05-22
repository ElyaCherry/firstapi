from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required
from models.users import UserModel


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank and it must exist!")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank and it must exist!")

    @staticmethod
    def post():
        user = UserRegisterResource.parser.parse_args()
        if UserModel.find_by_username(user.username):
            abort(409, message="User Already Exists")
        new_user = UserModel(**user)
        new_user.add_user()
        return {'message': f"added {user.username}"}, 201

    @jwt_required()
    def delete(self):
        user = UserRegisterResource.parser.parse_args()
        if UserModel.find_by_username(user.username):
            user = UserModel.query.filter_by(username=user.username)
            user.delete_user()
            return {'message': f"user removed"}, 204

        return {'message': f"user not found"}, 404
