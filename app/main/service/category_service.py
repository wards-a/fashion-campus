import copy, jwt, os

from flask_restx import abort

from app.main import db
from app.main.model.category import Category
from app.main.model.product import Product
from app.main.service.auth_service import get_user_by_id


def get_all_category(headers):
    current_user = _get_user_identity(headers)
    if current_user and current_user.type.value == "seller":
        result = db.session.execute(db.select(Category)).scalars()
    else:
        result = db.session.execute(db.select(Category).where(Category.deleted == "0")).scalars()
    return result.all()

def create_category(data):
    _validation(data)
    try:
        new_category = Category(
            name = data["category_name"]
        )
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    return {"message": "Category added"}, 201

def _validation(data: dict, category_id = None) -> dict:
    """
    Validations that json schema cannot handle.
    And format the data for the object at the same time.
    """
    result_data = copy.deepcopy(data)
    
    ########### Category unique based on name, category, and condition ###########
    category_exists = db.session.execute(db.select(Category).where(Category.deleted == '0').filter_by(name=result_data['category_name'])).first()
    # print(str(category_exists[0].id))
    # print(category_id)
    # print(str(category_exists[0]))
    if category_exists :
        if str(category_exists[0].id) != category_id:
            # if 'category_id' not in result_data:
                abort(400, 'There is already a category with that name')
            # if 'category_id' in result_data and result_data['category_id'] != str(category_exists[0].id):
            #     abort(400, 'There is already a category with that name')
        if category_id is None: 
            abort(400, 'There is already a category with that name')
    ### Rename properties to match database model ###
    result_data.update({'title': result_data.pop('category_name')})
    return result_data

def save_category_changes(data, category_id):    
    
    try:
        db.session.execute(
            db.update(Category)
            .where(Category.id == category_id)
            .values({"name":data["category_name"]})
        )
        db.session.flush()
    except:
        db.session.rollback()
        abort(500, "Category could not be updated")
    
    db.session.commit()

    return {"message": "Category updated"}, 200

def mark_as_deleted(category_id):
    try: 
        db.session.execute(db.select(Category).filter_by(id=category_id)).scalar_one()

    except db.exc.DataError:
        abort(404, "Category not available")

    product = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalar()
    if product:
        db.session.execute(db.update(Product).where(Product.category_id == category_id)).values({"category_id": None})
        db.session.commit()
    
    db.session.execute(db.delete(Category).where(Category.id == category_id))
    db.session.commit()

    return {"message": "Category deleted"}, 200

def _get_user_identity(headers):
    if "Authentication" in headers and headers["Authentication"]:
        user = jwt.decode(headers["Authentication"], os.environ.get('SECRET_KEY'), algorithms=["HS256"])
        current_user = get_user_by_id(user['id'])
        return current_user
    else:
        return None