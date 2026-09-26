from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import session
from app.models.user import User
from app.schemas.auth import AuthData, TokenData
from app.utils.security import to_hash, to_check_hash, encode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup(data: AuthData):
    try:
        async with session.begin() as ssn:
            result = await ssn.execute(select(User).where(User.username == data.username))
            if result.scalars().first():
                raise HTTPException(status_code=409, detail="user already exists")
            ssn.add(User(username=data.username, password=to_hash(data.password)))
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error")
    return {"message":"user added successfully, you can login"}

@router.post("/login", response_model=TokenData)
async def login(data: AuthData):
    try:
        async with session() as ssn:
            result = await ssn.execute(select(User.user_id, User.password).where(User.username == data.username))
            user = result.mappings().first()
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            if not to_check_hash(data.password, user["password"]):
                raise HTTPException(status_code=401, detail="not authorised")
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error")
    return {"access_token": encode_token(user["user_id"]), "token_type":"bearer"}
