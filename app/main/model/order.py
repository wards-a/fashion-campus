import enum

from app.main import db

class ShippingMethod(enum.Enum):
    REGULAR = "regular"
    NEXT_DAY = "next_day"

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    shipping_method = db.Column(
        db.Enum(ShippingMethod, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=db.func.now()
    )
    details = db.relationship("Detail", backref="order")

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"

    
class Detail(db.Model):
    __tablename__ = "order_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String, db.ForeignKey("order.id"))
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String, nullable=False)
    product = db.relationship("Product", backref="detail")


    def __repr__(self) -> str:
        return f"<order id: {self.order_id}, product id: {self.product_id}>"
