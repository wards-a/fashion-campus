import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from celery import Celery

from app.main.utils.error_handler import register_error_handler

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="FASHION CAMPUS API")
celery = Celery(__name__)
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    ### cors config ###
    cors.init_app(app)
    ### celery config ###
    app.config.update(CELERY_CONFIG={
        'broker_url': os.environ['CELERY_BROKER_URL'],
        'task_serializer': 'pickle',
        'result_serializer': 'pickle',
        'accept_content': ['application/json', 'application/x-python-serialize']
    })
    celery.conf.update(app.config['CELERY_CONFIG'])
    ### db config ###
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    db.init_app(app)
    ### migrate ###
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
    ### routing ###
    from app.main.utils import route
    for ns, r in route.routes.items():
        if ns.endswith('_ns'):
            api.add_namespace(r)
    app.register_blueprint(blueprint)

    register_error_handler(app)
    
    return app

app = create_app()
