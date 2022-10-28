from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .utils import postgres_cloud
from .controller.image_controller import image_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ytta7H8jK17Aj'
    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_cloud
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # blueprints api
    blueprints = [image_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app

app = create_app()
