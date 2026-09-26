from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import session
from app.core.dependencies import current_user
from app.schemas.chat import ChatData, ChatResponse
from app.services.chatbot import chat

router = APIRouter(prefix="/chat", tags=["AI Chat"])

@router.post("", response_model=ChatResponse)
async def chat_ai(data: ChatData, user_id: int = Depends(current_user)):
    try:
        async with session() as ssn:
            answer = await chat(ssn, user_id, data.message)
            return {"answer": answer}
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error")
