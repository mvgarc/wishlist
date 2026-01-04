from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User

app = FastAPI(title="Wishlist API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Wishlist API running"}
