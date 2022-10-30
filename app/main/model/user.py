import enum

from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class Role(enum.Enum):
    SELLER = "seller"
    BUYER = "buyer"

class Admin(enum.Enum):
    NO = '0'
    YES = '1'


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name = db.Column(db.String, nullable=False)
    type = db.Column(
        db.Enum(Role, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    is_admin = db.Column(
        db.Enum(Admin, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(Admin.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, onupdate=db.func.now())
    address = db.relationship("ShippingAddress", backref="user")
    order = db.relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}, type: {self.role} \
            email: {self.email}> phone number: {self.phone_number}"
