from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class ShippingAddress(db.Model):
    __tablename__ = "shipping_address"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, onupdate=db.func.now())

    def __repr__(self) -> str:
        return f"id: {self.id}, user id: {self.user_id}, name: {self.name}"
