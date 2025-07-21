from datetime import datetime

from ..db import db

class PwnedPlatform(db.Model):
    __tablename__ = "pwned_platforms"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    domain = db.Column(db.String, nullable=False)
    breach_date = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Relationships
    email = db.relationship("Email", back_populates="breaches")
