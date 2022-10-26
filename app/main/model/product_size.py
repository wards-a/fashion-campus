import enum

from app.main import db

class Size(enum.Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"

class ProductSize(db.Model):
    __tablename__ = "product_size"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    size = db.Column(
        db.Enum(Size, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"product id: {self.product_id}, size: {self.size}"
        