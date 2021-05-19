from flask_restful import Resource, reqparse

from restful_v4.models.users import UserModel


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank and it must exist!")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank and it must exist!")

    @staticmethod
    def post():
        user = UserRegisterResource.parser.parse_args()
        if UserModel.find_by_username(user['username']):
            return {'message': f"user {user['username']} already exists"}, 400
        new_user = UserModel(username=user['username'], password=user['password'])
        new_user.add_user()
        return {'message': f"added user '{user['username']}'"}, 201

    @staticmethod
    def delete():
        user = UserRegisterResource.parser.parse_args()
        if UserModel.find_by_username(user['username']):
            user = UserModel.query.filter_by(username=user['username'])
            user.delete_user()
            return {'message': f"user '{user}' was deleted successfully"}, 204
        return {'message': f"user '{user}' does not exist"}, 404
