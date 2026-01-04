from fastapi import FastAPI

app = FastAPI(title="Wishlist API")

@app.get("/")
def root():
    return {
        "message": "Wishlist API running"
    }
