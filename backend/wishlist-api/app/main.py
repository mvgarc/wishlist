from fastapi import FastAPI
from app.models import user
from app.routes.auth import router as auth_router
from app.db.base import init_db

app = FastAPI(title="Wishlist API")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Wishlist API running"}
