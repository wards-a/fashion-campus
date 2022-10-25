from app.main import db

class Banner(db.Model):
    __tablename__ = "banner"

    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<id {self.id}>"