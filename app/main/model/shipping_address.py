from app.main import db

class ShippingAddress(db.Model):
    __tablename__ = "shipping_address"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f"id: {self.id}, user id: {self.user_id}, name: {self.name}"
