import enum

from app.main import db

class ProductCondition(enum.Enum):
    NEW = "new"
    USED = "used"

class IsDelete(enum.Enum):
    NO = "0"
    YES = "1"

class ProductSize(enum.Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"

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
    is_deleted = db.Column(
        db.Enum(IsDelete, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(IsDelete.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, onupdate=db.func.now())
    size = db.relationship("Size", backref="product")
    image = db.relationship("Image", backref="product")
    category = db.relationship("Category", backref="product")

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}, condition: {self.condition},> \
            price: {self.price}"


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"id: <{self.id}, name: {self.name}>"


class Size(db.Model):
    __tablename__ = "product_size"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    size = db.Column(
        db.Enum(ProductSize, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"product id: {self.product_id}, size: {self.size}"


class Image(db.Model):
    __tablename__ = "product_image"

    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    image = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "primary_key": [image]
    }

    def __repr__(self) -> str:
        return f"<id: {self.id}, image url: {self.image}>"