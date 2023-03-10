from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db
from app.main.model.enum_model import Deleted


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name = db.Column(db.String, nullable=False)
    deleted = db.Column(
        db.Enum(Deleted, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(Deleted.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    product = db.relationship('Product', back_populates="category", lazy="noload")

    def __repr__(self) -> str:
        return "<Category(id={}, name={}, created_at={}, updated_at={}, product={})>".format(
            self.id,
            self.name,
            self.created_at,
            self.updated_at,
            self.product
        )
