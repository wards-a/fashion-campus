from app.main import db
from app.main.model.category import Category

def get_all_categories():
    result = db.session.execute(db.select(Category).order_by(Category.created_at.desc())).all()
    print(result)
    print("+++++++")
    result = [e[0] for e in result]
    print(result[0])
    return result