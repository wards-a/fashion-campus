from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product
from app.main.model.product_image import ProductImage
from app.main.model.order_detail import OrderDetail

def get_home_categories():
    categories = db.session.execute(
        db.select(Category)
        .where(Category.deleted == "0")
        .order_by(Category.created_at.desc())
        .limit(4)
    ).scalars().all()

    for e in categories:
        image = db.session.execute(
            db.select(ProductImage.image)
            .join(Product)
            .join(Category)
            .filter(
                Category.id==e.id,
                Product.deleted=="0"
            )
        ).scalar()

        if image:
            setattr(e, 'image', image)
        else:
            setattr(e, 'image', '')
    return categories

def get_banner():
    latest_added = db.session.execute(
        db.select(Product)
        .join(Category)
        .filter(db.and_(Product.deleted == "0", Category.deleted == "0"))
        .order_by(Product.created_at.desc())
    ).scalar()
    most_sold = db.session.execute(
        db.select(Product, db.func.sum(OrderDetail.quantity).label("total_quantity"))
        .join(Product)
        .join(Category)
        .filter(db.and_(Product.deleted == "0", Category.deleted == "0"))
        .order_by(db.desc("total_quantity"))
        .group_by(Product.id)
    ).scalar()

    banner = list()
    if latest_added:
        banner.append(latest_added)
    if most_sold and most_sold.id != latest_added.id:
        banner.append(most_sold)

    return banner
