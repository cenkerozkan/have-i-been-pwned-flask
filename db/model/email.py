from datetime import datetime
from sqlalchemy.orm import relationship
from ..db import db


class Email(db.Model):
    __tablename__ = "emails"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),  # cascade at DB level
        nullable=False,
    )
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Relationships
    user = relationship("User", back_populates="emails")
    pwned_platforms = relationship(
        "PwnedPlatform",
        back_populates="email",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
