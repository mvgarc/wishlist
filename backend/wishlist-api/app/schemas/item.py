from pydantic import BaseModel
from app.models.item import EstadoItem

class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    url: str | None = None
    cantidad: int = 1

class ItemUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    url: str | None = None
    cantidad: int | None = None
    estado: EstadoItem | None = None

class ItemResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    url: str | None
    cantidad: int
    estado: EstadoItem

    class Config:
        from_attributes = True