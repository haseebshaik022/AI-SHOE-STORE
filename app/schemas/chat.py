from pydantic import BaseModel

class ChatData(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
