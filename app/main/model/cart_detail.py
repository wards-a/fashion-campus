from app.main import db

class CartDetail(db.Model):
    __tablename__ = "cart_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_id = db.Column(db.String, db.ForeignKey("cart.id"))
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<card id: {self.card_id}, product id: {self.product_id}>"
        