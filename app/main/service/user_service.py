import re

from flask import abort

from app.main import db
from app.main.model.user import User
from app.main.model.shipping_address import ShippingAddress


def get_user_balance(id):
    result = db.session.execute(db.select(User.balance).filter_by(id=id)).scalar()
    return result

def get_user_shipping_address(id):
    result = db.session.execute(db.select(ShippingAddress).filter_by(user_id=id)).scalar()
    if not result:
        abort(404, "Shipping address not available")
        
    # return ShippingAddress.__repr__(result)
    return {
        "id": str(result.id),
        "name": result.name,
        "phone_number": result.phone_number,
        "address": result.address,
        "city": result.city,
    }

def change_shipping_address(id, data):
    data['user_id'] = id
    
    shipping_address = db.session.execute(db.select(ShippingAddress).filter_by(user_id=id)).scalar()
    if shipping_address:
        # update
        db.session.execute(
            db.update(ShippingAddress)
            .where(ShippingAddress.user_id == id)
            .values(data)
        )
    else:
        # insert
        db.session.execute(
            db.insert(ShippingAddress)
            .values(data)
        )
    
    db.session.commit()
    
    return {"message": "Change shipping address success"}, 200

def top_up_balance(id, data):
    if 'amount' in data and data['amount'] > 0 :
        try:
            user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        except db.exc.NoResultFound:
            abort(404, "User not available")
        
        user.balance += data['amount']
        db.session.commit()
        
        return {"message": "Top Up balance success"}, 200
    
    abort(400, 'Invalid amount')
