from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.routes.auth import router as auth_router

app = FastAPI(title="Wishlist API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Wishlist API running"}
