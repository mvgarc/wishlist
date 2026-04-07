import secrets
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Lista(Base):
    __tablename__ = "listas"

    id            = Column(Integer, primary_key=True, index=True)
    titulo        = Column(String, nullable=False)
    descripcion   = Column(String, nullable=True)
    share_token   = Column(String, unique=True, index=True,
                           default=lambda: secrets.token_urlsafe(10))
    es_publica    = Column(Boolean, default=True)
    owner_id      = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner  = relationship("User", back_populates="listas")
    items  = relationship("Item", back_populates="lista", cascade="all, delete")