from email.policy import default
import enum
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app.main import db

class ProductCondition(enum.Enum):
    NEW = "new"
    USED = "used"

class IsDelete(enum.Enum):
    NO = "0"
    YES = "1"

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid4
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    # static size
    size = db.Column(db.String, nullable=False, server_default=str('[S, M, L, XL]'))
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(
        db.Enum(ProductCondition, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    is_deleted = db.Column(
        db.Enum(IsDelete, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(IsDelete.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, onupdate=db.func.now())
    image = db.relationship("ProductImage", backref="product")
    product_category = db.relationship("ProductCategory", back_populates="product")

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}, condition: {self.condition},> \
            price: {self.price}"
