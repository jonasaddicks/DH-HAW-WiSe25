from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .base import Base

class CommentModel(Base):
    __tablename__ = "comment"

    comment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    # PostGIS Point (SRID 4326 = WGS84)
    geom = Column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship("UserModel", back_populates="comments")