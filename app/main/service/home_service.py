from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product
from app.main.model.order_detail import OrderDetail

def get_home_categories():
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
        if product:
            setattr(e, 'images', product[0].images)
        else:
            setattr(e, 'images', '')

    return category

def get_banner():
    latest = db.session.execute(db.select(Product).order_by(Product.created_at.desc())).first()
    best_seller = db.session.execute(
        db.select(Product, db.func.count(OrderDetail.product_id).label("best_seller"))
        .join(Product)
        .order_by(db.desc("best_seller"))
        .group_by(Product.id)
    ).first()

    banner = list()
    banner.append(latest[0])
    banner.append(best_seller[0])

    return banner
