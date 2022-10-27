from flask_migrate import Migrate

from app.main import app, db

from app.main.model import (
    address,
    banner,
    cart,
    order,
    product,
    role,
    user
)

Migrate(app, db)
