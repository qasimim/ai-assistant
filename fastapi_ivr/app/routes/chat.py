#chat.py
from fastapi.middleware.cors import CORSMiddleware
import logging

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from ..utils.rasa_utils import send_to_rasa

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    user_message = chat_request.message
    logger.info(f"Received chat message: {user_message}")
    try:
        reply_message = send_to_rasa("Caller_ID", user_message)
    except Exception as e:
        logger.error(f"Failed to send message to Rasa: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process message")
    return ChatResponse(reply=reply_message)
