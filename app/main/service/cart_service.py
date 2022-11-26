from flask import abort

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cart_detail import CartDetail


def get_cart(id):
    try:
        cart = db.session.execute(db.select(Cart).filter_by(user_id=id)).scalar()
        data = []
        if cart:
            for i in cart.details:
                temp = {
                    "id": str(i.id),
                    "details": {
                        "quantity": i.quantity,
                        "size": i.size
                    },
                    "price": int(i.product.price),
                    "image": i.product.images[0].image if i.product.images else "/image/default.jpg",
                    "name": i.product.name
                }
                data.append(temp)
        return {"status": True, "message": "Success", "data": data}, 200
    except Exception as e:
        return {"status": False, "message": str(e), "data": []}, 500

def add_cart(id, data):
    try:
        cart = db.session.execute(db.select(Cart).filter_by(user_id=id)).scalar()
        if not cart:
            # create cart & insert cart_detail
            cart_data = {"user_id": id}
            db.session.execute(db.insert(Cart).values(cart_data))
            db.session.commit()
        
        # get cart_id
        cart_id = db.session.execute(db.select(Cart.id).filter_by(user_id=id)).scalar()
        
        # check cart_detail
        cart_detail = db.session.execute(db.select(CartDetail).filter_by(cart_id=cart_id,product_id=data['id'],size=data['size'])).scalar()
        if cart_detail:
            # update quantity
            cart_detail_data = {"quantity": data['quantity']}
            db.session.execute(
                db.update(CartDetail)
                .where(CartDetail.id == cart_detail.id)
                .values(cart_detail_data)
            )
            db.session.commit()
        else:
            cart_detail_data = {
                "cart_id": cart_id,
                "product_id": data['id'],
                "size": data['size'],
                "quantity": data['quantity']
            }
            db.session.execute(db.insert(CartDetail).values(cart_detail_data))
            db.session.commit()
        
        return {"status": True, "message": "success added item to cart"}, 200
    except Exception as e:
        return {"status": False, "message": str(e)}, 500

def delete_cart(id, cart_id):
    try:
        # return str(db.delete(CartDetail).where(CartDetail.id == str(cart_id)))
        
        db.session.execute(db.delete(CartDetail).where(CartDetail.id == cart_id))
        db.session.commit()
        
        cart = db.session.execute(db.select(Cart).filter_by(user_id=id)).scalar()
        if not cart:
            db.session.execute(db.delete(Cart).where(Cart.user_id == id))
            db.session.commit()
        
        return {"status": True, "message": "Cart deleted"}, 200
    except Exception as e:
        return {"status": False, "message": str(e)}, 500

def delete_cart_by_product(product_id):
    try:
        cart_detail = db.session.execute(db.select(CartDetail).filter_by(product_id=product_id)).all()
        if cart_detail:
            cart_id_list = []
            for i in cart_detail:
                cart_id_list.append(i[0].cart_id)
            
            db.session.execute(db.delete(CartDetail).where(CartDetail.product_id == product_id))
            db.session.commit()
            for cart_id in cart_id_list:
                cart = db.session.execute(db.select(Cart).filter_by(id=cart_id)).scalar()
                if not cart.details:
                    db.session.execute(db.delete(Cart).where(Cart.id == cart_id))
                    db.session.commit()
        return {"status": True, "message": "Success"}, 200
    except Exception as e:
        return {"status": False, "message": str(e)}, 500
