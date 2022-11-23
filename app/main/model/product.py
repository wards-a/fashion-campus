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
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id', ondelete="SET NULL"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    # static size
    size = db.Column(db.ARRAY(db.String), nullable=False, server_default="{S, M, L, XL}")
    price = db.Column(db.Numeric(12, 2), nullable=False)
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
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    images = db.relationship("ProductImage", backref="product")
    category = db.relationship('Category', back_populates='product')

    def __repr__(self):
        return "<Product(id={}, name={}, description={}, size={}, price={}, condition={}, " \
            "is deleted={}, created_at={}, updated_at={}, category_id={})>".format(
            self.id,
            self.name,
            self.description,
            self.size,
            self.price,
            self.condition,
            self.is_deleted,
            self.created_at,
            self.updated_at,
            self.category_id
        )
