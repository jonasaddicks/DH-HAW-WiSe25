from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.database import Base

class User(Base):
    __tablename__ = "user"

    # PK: UUID
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Attributes
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.UTC, nullable=False)
    updated_at = Column(DateTime, default=datetime.UTC, onupdate=datetime.UTC, nullable=False)

    # Relationships
    preferences = relationship(
        "UserPrefs",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    contributions = relationship(
        "Contribution",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email}, display_name={self.display_name})>"