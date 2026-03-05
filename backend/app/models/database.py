import asyncio
import os
import aiosqlite
from app.config import settings

async def init_session_db():
    os.makedirs(os.path.dirname(settings.SESSION_DB_PATH), exist_ok=True)
    async with aiosqlite.connect(settings.SESSION_DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
                role TEXT CHECK(role IN ('user', 'assistant')),
                content TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_db_connection(db_path: str):
    return await aiosqlite.connect(db_path)
