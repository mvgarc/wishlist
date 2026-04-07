from app.db.session import engine , Base
from app.models.user import User
from app.models.lista import Lista
from app.models.item import Item

def init_db():
    Base.metadata.create_all(bind=engine)
