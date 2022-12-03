from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app.main import db
from app.main.model.enum_model import Deleted


class Banner(db.Model):
    __tablename__ = 'banner'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.String, nullable=False)
    deleted = db.Column(
        db.Enum(Deleted, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        server_default=str(Deleted.NO.value)
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return "<Banner(id={}, title={}, image={}, is deleted={}, created_at={}, updated_at={}, category_id={})>".format(
            self.id,
            self.title,
            self.image,
            self.deleted,
            self.created_at,
            self.updated_at
        )