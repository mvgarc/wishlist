from app.core.security import hash_password
from app.schemas.user import UserCreate

def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        nombre=data.nombre,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
