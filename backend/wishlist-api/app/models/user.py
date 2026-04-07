from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String, nullable=False)
    email    = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    listas   = relationship("Lista", back_populates="owner", cascade="all, delete")