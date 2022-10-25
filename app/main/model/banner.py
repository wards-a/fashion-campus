from app.main import db

class Banner(db.Model):
    __tablename__ = "banner"

    id = db.Column(db.String, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<id: {self.id}, title: {self.title}>"
