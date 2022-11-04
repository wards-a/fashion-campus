from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class ProductImage(db.Model):
    __tablename__ = "product_image"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    product = db.relationship("Product", back_populates="images")

    def __repr__(self) -> str:
        return "<ProductImage(id={}, image={}, created_at={})>".format(
            self.id,
            self.image,
            self.created_at
        )
