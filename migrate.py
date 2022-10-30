from flask_migrate import Migrate

from app.main import app, db

from app.main.model import (
    user,
    shipping_address,
    product,
    product_image,
    category,
    cart,
    cart_detail,
    order,
    order_detail
)

Migrate(app, db)
