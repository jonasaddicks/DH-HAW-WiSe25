from sqlalchemy import Column, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class Contribution(Base):
    __tablename__ = "contribution"

    # PK: bigint serial
    contrib_id = Column(BigInteger, primary_key=True, autoincrement=True)

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
    target_table = Column(String(100), nullable=False)
    target_id = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)  # 'create', 'update', 'delete', 'verify'
    details = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="contributions")
    poi = relationship("PointOfInterest", back_populates="contributions")

    def __repr__(self):
        return f"<Contribution(contrib_id={self.contrib_id}, action={self.action}, target_table={self.target_table})>"
