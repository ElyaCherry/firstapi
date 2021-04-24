from users import User

'''# Users table
users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcdef'),
]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
'''


# Authorization methods
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and (user.password == password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
