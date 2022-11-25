from sqlalchemy.sql import label

from app.main import db
from app.main.model.order import Order


def get_total_sales():
    total_sales = 0
    try:
        order = db.session.execute(db.select(Order)).all()
        # calculate total sales
        for data in order[0]:
            total_sales += data.shipping_price
            total_sales += int(sum([float(detail.quantity * detail.price) for detail in data.details]))
        
        return {"status": True, "message": "Success", "data": [{"total": int(total_sales)}]}, 200
    except IndexError:
        return {"status": True, "message": "Index out of range", "data": [{"total": total_sales}]}, 200
