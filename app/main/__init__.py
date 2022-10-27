from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .utils import postgres_cloud
from .controller.universal.image import image_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_cloud
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints api
    blueprints = [image_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app

app = create_app()
