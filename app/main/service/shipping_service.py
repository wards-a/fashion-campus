from flask import abort

from app.main import db
from app.main.model.cart import Cart
from app.main.model.user import User
from app.main.model.shipping_address import ShippingAddress
from app.main.service.cart_service import (
    get_cart
)


def get_shipping_price(id):
    try:
        cart = get_cart(id)
        # check cart is empty
        if not cart.data:
            return {"status": True, "message": "Don't have a cart", "data": []}, 200
        
        # calculate total price
        total_price = sum([float(detail.quantity * detail.product.price) for detail in cart.details])
        shipping_method = [{"name": "regular", "price": 0},{"name": "next day", "price": 0}]
        
        # calculate regular price
        regular_price = (15*total_price)/100 if total_price < 200 else (20*total_price)/100
        shipping_method[0]["price"] = int(regular_price)
        # calculate next day
        next_day_price = (20*total_price)/100 if total_price < 300 else (25*total_price)/100
        shipping_method[1]["price"] = int(next_day_price)
        
        return {"status": True, "message": "Success", "data": shipping_method}, 200
    except Exception as e:
        return {"status": False, "message": str(e), "data": []}, 500
