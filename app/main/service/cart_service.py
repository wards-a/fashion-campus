from flask import abort

from app.main import db
from app.main.model.cart import Cart


def get_user_cart(id):
    result = db.session.execute(db.select(Cart).filter_by(user_id=id)).scalar()
    return result
