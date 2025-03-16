from sqlalchemy import String, Column, BigInteger, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from bot.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    id_chat = Column(BigInteger, index=True)

    notes = relationship("Note", back_populates='user')


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    term = Column(DateTime, index=True)
    reminder = Column(DateTime, index=True)
    content = Column(String(256))
    user_id = Column(Integer, ForeignKey("user.id"))
    overdue = Column(Boolean, default=False)

    user = relationship("User", back_populates="notes")