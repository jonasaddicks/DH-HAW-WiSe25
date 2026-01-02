from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class UserPrefs(Base):
    __tablename__ = "userprefs"

    # PK & FK
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    # Attributes
    prefs = Column(JSON, nullable=False, default={})
    updated_at = Column(DateTime, default=datetime.UTC, onupdate=datetime.UTC, nullable=False)

    # Relationship
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPrefs(user_id={self.user_id})>"