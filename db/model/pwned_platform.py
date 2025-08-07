from datetime import datetime

from ..db import db

class PwnedPlatform(db.Model):
    __tablename__ = "pwned_platforms"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    title = db.Column(db.String, nullable=True)
    domain = db.Column(db.String, nullable=False)
    breach_date = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now())
    descripiton = db.Column(db.String, nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    email = db.relationship("Email", back_populates="breaches")
