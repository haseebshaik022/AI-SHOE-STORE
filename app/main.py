from fastapi import FastAPI
from app.api import auth, items, orders, chat
import app.models

app = FastAPI(title="AI Shoe Store Backend")
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(orders.router)
app.include_router(chat.router)

@app.get("/")
async def home():
    return {"message":"AI Shoe Store Backend", "docs":"/docs"}
