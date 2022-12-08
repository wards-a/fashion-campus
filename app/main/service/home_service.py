import io

from app.main import db
from app.main.model.category import Category
from app.main.model.banner import Banner
from app.main.model.product import Product
from app.main.model.product_image import ProductImage

from app.main.utils.image_helper import secure_name, b64str_to_byte
from app.main.utils.celery_tasks import upload_to_gcs, remove_from_gcs


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

def save_new_banner(data):
    new_banner = Banner(title=data['title'], image=data['title'])
    try:
        db.session.add(new_banner)
        db.session.flush()
        banner_name = _upload_banner(data)
        new_banner.image = banner_name
    except db.exc.IntegrityError as e:
        db.session.rollback()
        return {"message": "Banner could not be added", "error": str(e.orig)}, 400
    
    db.session.commit()
    return {"message": "Banner added"}, 201

def delete_banner(id):
    try:
        image = db.session.execute(
            db.delete(Banner)
            .where(Banner.id==id)
            .returning(Banner.image)
        ).scalar()
        remove_from_gcs.apply_async(args=[image], countdown=3)
    except db.session.DataError as e:
        return {"message": "Banner cannot be deleted", "error": str(e.orig)}, 400
    
    db.session.commit()
    return {"message": "Banner deleted"}

def _upload_banner(data):
    b64_str = data['image']
    title = secure_name(data['title'])

    media_type = b64_str.split(',')[0]
    media_type = media_type[media_type.find(':')+1 : media_type.find(';')]
    extension = media_type.split('/')[1]
    extension = 'jpg' if extension=='jpeg' else extension

    result_byte = b64str_to_byte(b64_str)
    
    img_io = io.BytesIO(result_byte)
    img_io.seek(0)
    image = {
        "filename": title+'.'+extension,
        "media_type": media_type,
        "file": img_io
    }

    upload_to_gcs.apply_async(args=[image], countdown=3)

    return image['filename']