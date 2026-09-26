import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def to_hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def to_check_hash(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def encode_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"user_id": user_id, "exp": expire}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str):
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    return int(payload["user_id"])
