from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from .base import Base

class UserPrefsModel(Base):
    __tablename__ = "user_prefs"

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    prefs = Column(
        JSON,
        nullable=False,
        default=dict
    )

    user = relationship("UserModel", back_populates="prefs")
