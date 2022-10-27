from app.main import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"id: <{self.id}, name: {self.name}>"
