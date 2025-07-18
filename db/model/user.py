from datetime import datetime

from ..db import db

class User(db.Model):
    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Relationships
    emails = db.relationship("Email", back_populates="user", cascade="all, delete")