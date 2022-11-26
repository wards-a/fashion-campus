from flask_restx import abort

from app.main import db
from app.main.model.user import User
from app.main.model.order import Order
from app.main.model.shipping_address import ShippingAddress


def get_user_balance(id):
    try:
        balance = db.session.execute(db.select(User.balance).filter_by(id=id)).scalar()
        return {"status": True, "message": "Success", "data": {"balance": int(balance)}}, 200
    except Exception as e:
        return {"status": False, "message": str(e), "data": {}}, 500

def get_user_shipping_address(id):
    result = db.session.execute(db.select(ShippingAddress).filter_by(user_id=id)).scalar()
    if not result:
        abort(404, "Shipping address not available")
    
    return {"status": True, "message": "Success", "data": {
        "id": str(result.id),
        "name": result.name,
        "phone_number": result.phone_number,
        "address": result.address,
        "city": result.city,
    }}, 200

def change_shipping_address(id, data):
    try:
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
        
        return {"status": True, "message": "Change shipping address success"}, 200
    except Exception as e:
        return {"status": False, "message": str(e)}, 500

def top_up_balance(id, data):
    try:
        if 'amount' in data and data['amount'] > 0 :
            try:
                user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
            except db.exc.NoResultFound:
                abort(404, "User not available")
            
            user.balance += data['amount']
            db.session.commit()
            
            balance = db.session.execute(db.select(User.balance).filter_by(id=id)).scalar()
            
            return {"status": True, "message": "Top Up balance success", "data": {"balance": int(balance)}}, 200
        
        abort(400, 'Invalid amount')
    except Exception as e:
        return {"status": False, "message": str(e)}, 500

def get_user_order(user_id):
    result = db.session.execute(db.select(Order).where(Order.user_id==user_id)).all()
    order = [e[0] for e in result]
    return order