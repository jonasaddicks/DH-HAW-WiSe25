from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

from .base import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    comments = relationship(
        "CommentModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    prefs = relationship(
        "UserPrefsModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
