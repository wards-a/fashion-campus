from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class CartDetail(db.Model):
    __tablename__ = "cart_detail"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'))
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=db.func.now()
    )
    product = db.relationship("Product", backref="detail")

    def __repr__(self) -> str:
        return "<CartDetail(id={}, size={}, quantity={}, created_at={}, updated_at={} " \
            "product.name={})>".format(
            self.id,
            self.size,
            self.quantity,
            self.created_at,
            self.updated_at,
            self.product.name
        )
