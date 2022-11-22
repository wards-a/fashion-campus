from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product

def get_all_categories():
    category = db.session.execute(
        db.select(Category)
        .order_by(Category.created_at.desc())
        .limit(4)
        .options(db.noload(Category.product))
    ).all()

    category = [e[0] for e in category]
    category_id = [e.id for e in category]

    product = db.session.execute(
        db.select(Product)
        .distinct(Product.category_id)
        .filter(Product.category_id.in_(category_id))
    ).all()

    products = [e[0] for e in product]

    for e in category:
        product = [i for i in products if i.category_id==e.id]
        setattr(e, 'images', product[0].images)
        
    return category
