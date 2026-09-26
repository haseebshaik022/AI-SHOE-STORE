from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import decode_token

bearer = HTTPBearer()

async def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        return decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
