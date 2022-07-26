from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25))
    fullname = Column(String(40))
    email = Column(String(30))
    password = Column(String(130))
    profile_image = Column(Integer, ForeignKey("images.id"))

    blogs = relationship("Blog", back_populates="writer")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(120), nullable=True)
    date = Column(Date)
    content = Column(String(2400))
    writer_id = Column(Integer, ForeignKey("users.id"))

    writer = relationship("User", back_populates="blogs")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(50))
