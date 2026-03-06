from fastapi import APIRouter, Depends, Query, Path
from typing import List
from aiosqlite import Connection

from app.models.schemas import SessionResponse, SessionDetailResponse, SessionCreate
from app.models.database import get_db_connection
from app.services.session_service import SessionService

router = APIRouter()

def get_session_service(db: Connection = Depends(get_db_connection)) -> SessionService:
    return SessionService(db)

@router.get("", response_model=List[SessionResponse])
async def list_sessions(service: SessionService = Depends(get_session_service)):
    """List all sessions ordered by updated_at descending."""
    return await service.get_all_sessions()

@router.post("", response_model=SessionResponse)
async def create_session(data: SessionCreate, service: SessionService = Depends(get_session_service)):
    """Create a new chat session."""
    return await service.create_session(title=data.title)

@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str = Path(...), service: SessionService = Depends(get_session_service)):
    """Get session details including message history."""
    return await service.get_session_detail(session_id)

@router.delete("/{session_id}")
async def delete_session(session_id: str = Path(...), service: SessionService = Depends(get_session_service)):
    """Delete a session by ID."""
    await service.delete_session(session_id)
    return {"status": "success"}

@router.put("/{session_id}/title")
async def update_title(title: str = Query(..., description="The new title"), session_id: str = Path(...), service: SessionService = Depends(get_session_service)):
    """Update session title."""
    await service.update_session_title(session_id, title)
    return {"status": "success"}
