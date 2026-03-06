import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Session Models
class SessionBase(BaseModel):
    title: str = "New Chat"

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

# Message Models
class MessageBase(BaseModel):
    role: str # 'user' or 'assistant'
    content: str
    metadata: Optional[Dict[str, Any]] = None # stores SQL queries, data, charts

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    session_id: str
    created_at: datetime

# Combined Model
class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse] = []
