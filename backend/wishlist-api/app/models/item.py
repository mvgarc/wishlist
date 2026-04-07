from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class EstadoItem(str, enum.Enum):
    pendiente  = "pendiente"
    reservado  = "reservado"
    comprado   = "comprado"

class Item(Base):
    __tablename__ = "items"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    url         = Column(String, nullable=True)   # link al producto
    cantidad    = Column(Integer, default=1)
    estado      = Column(Enum(EstadoItem), default=EstadoItem.pendiente)
    lista_id    = Column(Integer, ForeignKey("listas.id"), nullable=False)

    lista = relationship("Lista", back_populates="items")