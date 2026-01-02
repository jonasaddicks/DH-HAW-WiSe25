from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from backend.app.database import Base

class POISource(str, Enum):
    """Enum für source-Feld"""
    OSM = "osm"
    USER = "user"
    IMPORT = "import"
    MOCK = "mock"

class PointOfInterest(Base):
    __tablename__ = "pointofinterest"

    # PK: bigint (für OSM-IDs)
    osm_id = Column(BigInteger, primary_key=True)

    # Attributes
    source = Column(
        SQLEnum(POISource, name="poi_source_enum", create_type=True),
        nullable=False
    )
    kind = Column(String(50), nullable=False, index=True)
    tags = Column(JSON, nullable=False, default={})
    geom = Column(String, nullable=False)  # PostGIS Point als String (WKT oder ähnlich)
    is_verified = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    comments = relationship(
        "Comment",
        back_populates="poi",
        cascade="all, delete-orphan"
    )

    contributions = relationship(
        "Contribution",
        back_populates="poi",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<PointOfInterest(osm_id={self.osm_id}, kind={self.kind}, source={self.source})>"