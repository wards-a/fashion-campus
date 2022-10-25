from flask_migrate import Migrate

from app.main import create_app, db

from app.main.model import banner

app = create_app()

migrate = Migrate(app, db)
