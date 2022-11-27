from flask_restx import abort

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cart_detail import CartDetail
from app.main.model.product import Product
from app.main.model.order import Order
from app.main.model.order_detail import OrderDetail
from app.main.model.user import User
from app.main.model.shipping_address import ShippingAddress


def create_order(data, user_id):
    shipping_method = data['shipping_method']
    address_name = data['shipping_address']['name']

    address_id = _get_address_id(user_id, address_name)
    cart = db.session.execute(
        db.select(Cart)
        .filter_by(user_id=user_id)
        .options(
            db.noload(Cart.details, CartDetail.product, Product.images)
        )
    ).scalar()
    subtotal = sum([float(detail.quantity * detail.product.price) for detail in cart.details])
    shipping_price = _calculate_shipping_price(shipping_method, subtotal)
    total_price = subtotal + shipping_price

    if int(cart.user.balance) < int(total_price):
        abort(400, "Insufficient balance")

    try:
        new_order = Order(
            user_id=user_id,
            shipping_address_id=address_id,
            shipping_method=shipping_method,
            shipping_price=shipping_price
        )
        db.session.add(new_order)
        db.session.flush()

        order_details = []
        for detail in cart.details:
            order_details.append(
                OrderDetail(
                    order_id = new_order.id,
                    product_id = detail.product_id,
                    size = detail.size,
                    quantity = detail.quantity,
                    price = detail.product.price
                )
            )
        db.session.add_all(order_details)
        db.session.flush()
    except:
        db.session.rollback()
        abort(500, "Order failed, something went wrong")
    
    db.session.execute(
        db.update(User)
        .where(User.id==user_id)
        .values(balance=int(cart.user.balance)-int(total_price))
    )

    db.session.delete(cart)

    db.session.commit()
    return {"message": "Order success"}


def get_all_orders():
    result = db.session.execute(
        db.select(Order)
        .options(db.joinedload(Order.user))
    ).scalars()
    
    orders = list()
    for e in result:
        total_price = e.shipping_price
        for d in e.details:
            total_price += d.quantity*d.price
        setattr(e, "total_price", total_price)
        orders.append(e)

    return orders

def _get_address_id(user_id, address_name):
    address_id = db.session.execute(
        db.select(ShippingAddress.id)
        .filter(
            db.and_(
                ShippingAddress.user_id == user_id,
                ShippingAddress.name == address_name
            )
        )
    ).scalar()

    return address_id

def _calculate_shipping_price(shipping_method, subtotal):
    shipping_price = None
    if shipping_method == "regular":
        shipping_price = (15*subtotal)/100 if subtotal < 200 else (20*subtotal)/100
    if shipping_method == "next day":
        shipping_price = (20*subtotal)/100 if subtotal < 300 else (25*subtotal)/100
    
    return shipping_price
