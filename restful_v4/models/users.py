from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(60))

    def __str__(self):
        return "User(id='%s')" % self.id

    def jsonify(self):
        return {"username": self.username, "password": self.password}

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(_username):
        return db.session.query(UserModel).filter_by(username=_username).first()

    @staticmethod
    def find_by_id(_id):
        return db.session.query(UserModel).filter_by(id=_id).first()
