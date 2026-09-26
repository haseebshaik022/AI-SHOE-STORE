# AI Shoe Store - Backend Only

Interview-focused FastAPI backend. No frontend and no admin system.

## Database
- users: user_id, username, password
- items: item_id, item_name, item_price
- orders: order_id, user_id -> users.user_id, item_id -> items.item_id
- policy_chunks: chunk_id, content, embedding (384)

## ORM rule
All database work uses SQLAlchemy ORM. The only raw SQL is `CREATE EXTENSION IF NOT EXISTS vector` in `preruns.py`.

## Auth
Signup -> login -> JWT. Every protected endpoint verifies `Authorization: Bearer <token>` and gets the user_id from the JWT.

## Run
Fill `.env` in this project root. Then run once:
```bash
python preruns.py
python add_items.py
```
Then:
```bash
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs
