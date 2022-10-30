import enum

from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class ShippingMethod(enum.Enum):
    SAME_DAY = "same day"
    NEXT_DAY = "next day"

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid4
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    shipping_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('shipping_address.id'))
    shipping_method = db.Column(
        db.Enum(ShippingMethod, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    user = db.relationship("User", back_populates="order")
    shipping_address = db.relationship("ShippingAddress", back_populates="shipping_address")
    details = db.relationship("OrderDetail", backref="order")

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"
