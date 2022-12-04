from app.main import db
from app.main.model.category import Category
from app.main.model.banner import Banner
from app.main.model.product import Product
from app.main.model.product_image import ProductImage

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
    result = db.session.execute(db.select(Banner).where(Banner.deleted=="0")).scalars().all()
    return result
    