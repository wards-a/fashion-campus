import enum

from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db
from app.main.model.enum_model import Role, Admin


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
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    # is_admin = db.Column(
    #     db.Enum(Admin, values_callable=lambda obj: [e.value for e in obj]),
    #     nullable=False,
    #     server_default=str(Admin.NO.value)
    # )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    address = db.relationship("ShippingAddress", backref="user")
    order = db.relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return "<User(id={}, name={}, type={}, email={}, phone_number={}, " \
            "balance={}, created_at={}, updated_at={})>".format(
                self.id,
                self.name,
                self.type,
                self.email,
                self.phone_number,
                self.balance,
                self.created_at,
                self.updated_at
        )
