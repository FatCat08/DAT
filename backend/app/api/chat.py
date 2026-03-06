from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.models.database import get_db_connection
from app.services.session_service import SessionService
from app.core.llm_chain import LLMChain
from aiosqlite import Connection

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

def get_session_service(db: Connection = Depends(get_db_connection)) -> SessionService:
    return SessionService(db)

@router.post("", response_class=StreamingResponse)
async def chat_endpoint(req: ChatRequest, service: SessionService = Depends(get_session_service)):
    chain = LLMChain(session_service=service)
    return StreamingResponse(
        chain.generate_response_stream(req.session_id, req.message), 
        media_type="text/event-stream"
    )
