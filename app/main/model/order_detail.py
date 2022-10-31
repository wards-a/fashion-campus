from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('order.id'))
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship("Product", backref="detail")


    def __repr__(self) -> str:
        return f"<order id: {self.order_id}, product id: {self.product_id}>"
