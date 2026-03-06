import sqlite3
import aiosqlite
import os

from app.config import get_settings

settings = get_settings()

def get_db_path() -> str:
    # Ensure directory exists
    os.makedirs(os.path.dirname(settings.SESSION_DB_PATH), exist_ok=True)
    return settings.SESSION_DB_PATH

async def init_db():
    """Initializes the SQLite database with sessions and messages tables."""
    db_path = get_db_path()
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
        """)
        await db.commit()

async def get_db_connection():
    """Dependency to get an async db connection."""
    db = await aiosqlite.connect(get_db_path())
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
