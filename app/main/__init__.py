from flask import Flask, got_request_exception
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from app.main.utils import postgres_cloud
from app.main.service.errors import custom_error_handler
from app.main.controller.image_controller import image_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    got_request_exception.connect(custom_error_handler, app)
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

@app.errorhandler(Exception)
def handle_exception(e):
    response = {"message": e.description}
    return response, e.code
