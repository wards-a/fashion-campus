from app.main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}, email: {self.email}> \
            phone number: {self.phone_number}"
