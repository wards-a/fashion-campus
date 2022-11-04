import os

from flask import Flask, Blueprint, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="FASHION CAMPUS API")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Y7H8jK17Aj'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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
    migrate.init_app(app, db)

    from app.main.controller.image_controller import image_ns
    from app.main.controller.home_controller import home_ns
    from app.main.controller.auth_controller import sign_up_ns, sign_in_ns
    from app.main.controller.products_controller import products_ns
    from app.main.controller.category_controller import category_ns
    from app.main.controller.cart_controller import cart_ns
    from app.main.controller.user_controller import user_ns
    from app.main.controller.shipping_controller import shipping_ns
    from app.main.controller.order_controller import order_ns, orders_ns
    from app.main.controller.sales_controller import sales_ns
    namespaces = [
        image_ns,
        home_ns,
        sign_up_ns,
        sign_in_ns,
        products_ns,
        category_ns,
        cart_ns,
        user_ns,
        shipping_ns,
        order_ns,
        orders_ns,
        sales_ns
    ]
    for ns in namespaces:
        api.add_namespace(ns)
    app.register_blueprint(blueprint)
    
    return app

app = create_app()

@app.errorhandler(Exception)
def handle_exception(e):
    # HTTP errors
    if isinstance(e, HTTPException):
        return {"message": e.description}, e.code

    # Non-HTTP, exceptions only
    return {"message": str(e)}, 500

@app.after_request
def after_request(response):
    """
    to "catch" flask_restx.errors.ValidationError

    masih belum di kustomisasi 
    """
    if int(response.status_code) == 404:
      response.set_data(json.dumps({'success': False, 'data': [],
                               'msg': 'Resource not found. Check Resouce URI again'}))

    if int(response.status_code) >= 400:
      response_data = json.loads(response.get_data())
      if 'errors' in response_data:
        response_data = {"message": "Please input the field"}
        response.set_data(json.dumps(response_data))
      response.headers.add('Content-Type', 'application/json')
    return response