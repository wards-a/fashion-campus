import enum

from app.main import db

class ProductCondition(enum.Enum):
    NEW = "new"
    USED = "used"

class IsDelete(enum.Enum):
    NO = "0"
    YES = "1"

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    category_id = db.Column(db.String, db.ForeignKey("category.id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(
        db.Enum(ProductCondition, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    size = db.Column(db.String, nullable=False)
    is_deleted = db.Column(
        db.Enum(IsDelete, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(IsDelete.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, onupdate=db.func.now())

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}, condition: {self.condition},> \
            price: {self.price}"
