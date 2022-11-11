import re

from flask import abort

from app.main import db, bcrypt
from app.main.model.user import User, Role


def get_user_by_email(email):
    result = db.session.execute(db.select(User).filter_by(email=email)).scalar()
    return result

def get_user_by_id(id):
    result = db.session.execute(db.select(User).filter_by(id=id)).scalar()
    return result

def save_new_user(data):
    try:
        new_user = User(
            name = data['name'],
            type = Role.BUYER.value,
            email = data['email'],
            phone_number = data['phone_number'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            balance = 0
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    return {"message": "success, user created"}, 201
