from sqlalchemy import Column, String, ForeignKey, DateTime, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Comment(Base):
    __tablename__ = "comment"

    # PK: serial (Auto-Increment)
    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # FK
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    osm_id = Column(
        BigInteger,
        ForeignKey("pointofinterest.osm_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Attributes
    text = Column(String(1000), nullable=False)
    geom = Column(String, nullable=False)  # PostGIS Point
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="comments")
    poi = relationship("PointOfInterest", back_populates="comments")

    def __repr__(self):
        return f"<Comment(comment_id={self.comment_id}, user_id={self.user_id}, osm_id={self.osm_id})>"
