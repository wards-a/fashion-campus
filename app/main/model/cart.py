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

    def __repr__(self) -> str:
        return f"<id: {self.id}>, buyer id: {self.user_id}"
