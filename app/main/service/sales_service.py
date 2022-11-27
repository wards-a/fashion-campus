from sqlalchemy.sql import label

from app.main import db
from app.main.model.order import Order


def get_total_sales():
    total_sales = 0
    try:
        order = db.session.execute(db.select(Order)).all()
        # calculate total sales
        if order:
            for data in order:
                total_sales += data[0].shipping_price
                total_sales += int(sum([float(detail.quantity * detail.price) for detail in data[0].details]))
        
        data = {
            "total": int(total_sales)
        }
        return {"status": True, "message": "Success", "data": data}, 200
    except IndexError:
        return {"status": True, "message": "Index out of range", "data": []}, 200
