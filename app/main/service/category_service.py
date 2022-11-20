from app.main import db
from app.main.model.category import Category

def get_all_category():
    result = db.session.execute(db.select(Category)).all()
    result = [e[0] for e in result]
    return result
