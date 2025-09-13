from datetime import datetime
from sqlalchemy.orm import relationship
import json
from typing import List
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
    _data_classes = db.Column('data_classes', db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now())

    # Relationships
    email = relationship("Email", back_populates="pwned_platforms")

    @property
    def data_classes(self) -> List[str]:
        """Get data classes as list"""
        return json.loads(self._data_classes) if self._data_classes else []

    @data_classes.setter
    def data_classes(self, value: List[str]) -> None:
        """Store data classes as JSON string"""
        self._data_classes = json.dumps(value) if value else None

    def __eq__(self, other):
        if not isinstance(other, PwnedPlatform):
            return False
        
        if self.name == other.name and self.breach_date == other.breach_date:
            return True
        
        return False

    def __hash__(self):
        return hash((self.name, self.breach_date))
    
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