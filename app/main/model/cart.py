from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.main import db


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid4
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        server_default=db.func.now()
    )
    user = db.relationship("User", backref="user")
    details = db.relationship("CartDetail", backref="cart")

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"
