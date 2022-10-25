from app.main import db

class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String, db.ForeignKey("order.id"))
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<order id: {self.order_id}, product id: {self.product_id}>"
        