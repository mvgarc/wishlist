from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.lista import Lista
from app.models.item import Item
from app.schemas.lista import ListaCreate,ListaUpdate, ListaResponse
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/lists", tags=["Listas"])

@router.get("", response_model=dict)
def mis_listas(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    total = db.query(Lista).filter(Lista.owner_id == user.id).count()
    listas = (
        db.query(Lista)
        .filter(Lista.owner_id == user.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": -(-total // size),  # ceil division
        "items": listas
    }

@router.post("", response_model=ListaResponse, status_code=201)
def crear_lista(
    data: ListaCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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

@router.patch("/{lista_id}", response_model=ListaResponse)
def editar_lista(
    lista_id: int,
    data: ListaUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lista = db.query(Lista).filter(Lista.id == lista_id, Lista.owner_id == user.id).first()
    if not lista:
        raise HTTPException(404, "Lista no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(lista, campo, valor)
    db.commit()
    db.refresh(lista)
    return lista

@router.delete("/{lista_id}", status_code=204)
def eliminar_lista(
    lista_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lista = db.query(Lista).filter(Lista.id == lista_id, Lista.owner_id == user.id).first()
    if not lista:
        raise HTTPException(404, "Lista no encontrada")
    db.delete(lista)
    db.commit()

@router.post("/{lista_id}/items", response_model=ItemResponse, status_code=201)
def agregar_item(
    lista_id: int,
    data: ItemCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lista = db.query(Lista).filter(Lista.id == lista_id, Lista.owner_id == user.id).first()
    if not lista:
        raise HTTPException(404, "Lista no encontrada")
    item = Item(**data.model_dump(), lista_id=lista_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/items/{item_id}", response_model=ItemResponse)
def actualizar_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db)
):
    # Público: quien recibe la lista puede marcar items
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item no encontrado")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(item, campo, valor)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}", status_code=204)
def eliminar_item(
    item_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Busca el item y verifica que el usuario sea dueño de la lista
    item = db.query(Item).join(Lista).filter(
        Item.id == item_id,
        Lista.owner_id == user.id
    ).first()
    if not item:
        raise HTTPException(404, "Item no encontrado")
    db.delete(item)
    db.commit()