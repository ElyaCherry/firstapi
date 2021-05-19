from restful_v4.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)

    def jsonify(self):
        return {'name': self.name, 'price': self.price}

    @staticmethod
    def get_item(name):
        item = ItemModel.query.filter_by(name=name).first()
        return item

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update_item(name, price):
        db.session.query(ItemModel).filter_by(name=name).update({'price': price})
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_items():
        return ItemModel.query.all()

    @staticmethod
    def delete_items():
        db.session.query(ItemModel).delete()
        db.session.commit()
