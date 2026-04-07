from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.listas import router as listas_router
from app.db.base import init_db

app = FastAPI(title="Wishlist API - FastAPI", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router)
app.include_router(listas_router)

@app.get("/")
def root():
    return {"message": "Wishlist API running"}