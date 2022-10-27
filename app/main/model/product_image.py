from app.main import db

class ProducImage(db.Model):
    __tablename__ = "product_image"

    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    image = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "primary_key": [image_url]
    }

    def __repr__(self) -> str:
        return f"<id: {self.id}, image url: {self.image_url}>"
