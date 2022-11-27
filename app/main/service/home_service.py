from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product
from app.main.model.order_detail import OrderDetail

def get_home_categories():
    categories = db.session.execute(
        db.select(Category)
        .where(Category.deleted == "0")
        .order_by(Category.created_at.desc())
        .limit(4)
    ).scalars().all()

    category_id = [e.id for e in  categories]

    products = db.session.execute(
        db.select(Product)
        .distinct(Product.category_id)
        .filter(db.and_(Product.category_id.in_(category_id), Product.deleted=="0"))
    ).scalars()

    for e in categories:
        product = [i for i in products if i.category_id==e.id]
        if product:
            setattr(e, 'images', product[0].images)
        else:
            setattr(e, 'images', '')

    return categories

def get_banner():
    latest_added = db.session.execute(
        db.select(Product)
        .join(Category)
        .filter(db.and_(Product.deleted == "0", Category.deleted == "0"))
        .order_by(Product.created_at.desc())
    ).scalar()
    most_sold = db.session.execute(
        db.select(Product, db.func.count(OrderDetail.product_id).label("most_sold"))
        .join(Product)
        .join(Category)
        .filter(db.and_(Product.deleted == "0", Category.deleted == "0"))
        .order_by(db.desc("most_sold"))
        .group_by(Product.id)
    ).scalar()

    banner = list()
    if latest_added:
        banner.append(latest_added)
    if most_sold:
        banner.append(most_sold)

    return banner
