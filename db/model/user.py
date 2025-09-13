from datetime import datetime
from sqlalchemy.orm import relationship
from ..db import db


class User(db.Model):
    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Relationships
    emails = relationship(
        "Email",
        back_populates="user",
        cascade="all, delete-orphan",  # ensures child rows deleted
        passive_deletes=True,
    )
