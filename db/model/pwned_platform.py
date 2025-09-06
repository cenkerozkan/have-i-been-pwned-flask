from datetime import datetime
from sqlalchemy.orm import relationship
from ..db import db

class PwnedPlatform(db.Model):
    __tablename__ = "pwned_platforms"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(
        db.Integer,
        db.ForeignKey("emails.id", ondelete="CASCADE"),  # cascade at DB level
        nullable=False
    )
    name = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    domain = db.Column(db.String, nullable=False)
    breach_date = db.Column(db.Date, nullable=False)
    added_date = db.Column(db.DateTime, nullable=True, default=datetime.now())
    description = db.Column(db.String, nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now())

    # Relationships
    email = relationship("Email", back_populates="pwned_platforms")
    
    def to_json(self):
        """Convert model fields to a dictionary"""
        return {
            "id": self.id,
            "email_id": self.email_id,
            "name": self.name,
            "title": self.title,
            "domain": self.domain,
            "breach_date": self.breach_date.isoformat() if self.breach_date else None,
            "added_date": self.added_date.isoformat() if self.added_date else None,
            "description": self.description,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }