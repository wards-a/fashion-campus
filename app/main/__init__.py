import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from app.main.model.creds import pg_creds

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    return app