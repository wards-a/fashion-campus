
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))
    product = db.relationship('Product', back_populates='product_category')
    category = db.relationship('Category', back_populates='product_category')

    def __repr__(self) -> str:
        return f"product id: {self.product_id}, category id: {self.category_id}"
