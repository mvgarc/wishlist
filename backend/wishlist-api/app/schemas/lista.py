from pydantic import BaseModel
from app.schemas.item import ItemResponse

class ListaCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    es_publica: bool = True

class ListaUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    es_publica: bool | None = None

class ListaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    share_token: str
    es_publica: bool
    items: list[ItemResponse] = []

    class Config:
        from_attributes = True