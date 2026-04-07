from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.lista import Lista
from app.models.item import Item
from app.schemas.lista import ListaCreate, ListaResponse
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/lists", tags=["Listas"])

@router.get("", response_model=list[ListaResponse])
def mis_listas(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Lista).filter(Lista.owner_id == user.id).all()

@router.post("", response_model=ListaResponse, status_code=201)
def crear_lista(data: ListaCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lista = Lista(**data.model_dump(), owner_id=user.id)
    db.add(lista)
    db.commit()
    db.refresh(lista)
    return lista

@router.get("/share/{token}", response_model=ListaResponse)
def lista_publica(token: str, db: Session = Depends(get_db)):
    lista = db.query(Lista).filter(Lista.share_token == token).first()
    if not lista or not lista.es_publica:
        raise HTTPException(404, "Lista no encontrada")
    return lista

@router.post("/{lista_id}/items", response_model=ItemResponse, status_code=201)
def agregar_item(lista_id: int, data: ItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lista = db.query(Lista).filter(Lista.id == lista_id, Lista.owner_id == user.id).first()
    if not lista:
        raise HTTPException(404, "Lista no encontrada")
    item = Item(**data.model_dump(), lista_id=lista_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/items/{item_id}", response_model=ItemResponse)
def actualizar_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    # Este endpoint es público (para que quien recibe la lista marque como comprado)
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item no encontrado")
    item.estado = data.estado
    db.commit()
    db.refresh(item)
    return item