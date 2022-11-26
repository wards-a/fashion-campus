from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product
from app.main.model.order_detail import OrderDetail

def get_home_categories():
    category = db.session.execute(
        db.select(Category)
        .where(Category.deleted == "0")
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
    latest = db.session.execute(
        db.select(Product)
        .join(Category)
        .filter(db.and_(Product.deleted == "0", Category.deleted == "0"))
        .order_by(Product.created_at.desc())
    ).first()
    most_sold = db.session.execute(
        db.select(Product, db.func.count(OrderDetail.product_id).label("most_sold"))
        .where(Product.deleted == "0")
        .join(Product)
        .order_by(db.desc("most_sold"))
        .group_by(Product.id)
    ).first()

    banner = list()
    if latest:
        banner.append(latest[0])
    if most_sold:
        banner.append(most_sold[0])

    return banner
