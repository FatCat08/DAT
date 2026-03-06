import uuid
import json
from datetime import datetime
from aiosqlite import Connection
from typing import List, Optional

from app.models.schemas import SessionResponse, SessionDetailResponse, MessageResponse
from fastapi import HTTPException

class SessionService:
    def __init__(self, db: Connection):
        self.db = db

    async def get_all_sessions(self) -> List[SessionResponse]:
        async with self.db.execute("SELECT id, title, created_at, updated_at FROM sessions ORDER BY updated_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [SessionResponse(**dict(row)) for row in rows]

    async def create_session(self, title: str = "New Chat") -> SessionResponse:
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        await self.db.execute(
            "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (session_id, title, now, now)
        )
        await self.db.commit()
        return SessionResponse(id=session_id, title=title, created_at=now, updated_at=now)

    async def get_session_detail(self, session_id: str) -> SessionDetailResponse:
        # Get session
        async with self.db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Session not found")
            session = dict(row)
            
        # Get messages
        async with self.db.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC", (session_id,)) as cursor:
            msg_rows = await cursor.fetchall()
            
        messages = []
        for msg in msg_rows:
            d = dict(msg)
            # Parse metadata if exists
            metadata_str = d.pop('metadata', None)
            d['metadata'] = json.loads(metadata_str) if metadata_str else None
            messages.append(MessageResponse(**d))
            
        return SessionDetailResponse(**session, messages=messages)

    async def delete_session(self, session_id: str):
        await self.db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        await self.db.commit()

    async def update_session_title(self, session_id: str, title: str):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        await self.db.execute("UPDATE sessions SET title = ?, updated_at = ? WHERE id = ?", (title, now, session_id))
        await self.db.commit()

    async def save_message(self, session_id: str, role: str, content: str, metadata: dict = None) -> MessageResponse:
        msg_id = str(uuid.uuid4())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        metadata_str = json.dumps(metadata) if metadata else None
        
        await self.db.execute(
            "INSERT INTO messages (id, session_id, role, content, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (msg_id, session_id, role, content, metadata_str, now)
        )
        # Update session updated_at
        await self.db.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
        await self.db.commit()
        
        return MessageResponse(
            id=msg_id, 
            session_id=session_id, 
            role=role, 
            content=content, 
            metadata=metadata, 
            created_at=now
        )
