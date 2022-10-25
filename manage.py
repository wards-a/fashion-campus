from flask_migrate import Migrate

from app.main import create_app, db

from app.main.model import (
    role,
    user,
    banner,
    category,
    product,
    product_image,
    cart,
    cart_detail,
    shipping_address,
    order,
    order_detail
)

app = create_app()

migrate = Migrate(app, db)
