from app.main import db

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=db.func.now()
    )
    details = db.relationship("Detail", backref="cart")

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"


class Detail(db.Model):
    __tablename__ = "cart_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_id = db.Column(db.String, db.ForeignKey("cart.id"))
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String, nullable=False)
    product = db.relationship("Product", backref="detail")

    def __repr__(self) -> str:
        return f"<card id: {self.card_id}, product id: {self.product_id}>"