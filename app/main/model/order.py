import enum

from app.main import db

class ShippingMethod(enum.Enum):
    REGULAR = "regular"
    NEXT_DAY = "next_day"

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    shipping_method = db.Column(
        db.Enum(ShippingMethod, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=db.func.now()
    )

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"
