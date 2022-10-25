from app.main import db

class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<id: {self.id}, name: {self.name}>"
