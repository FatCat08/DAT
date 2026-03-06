from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.database import init_db
from app.api.session import router as session_router
from app.api.chat import router as chat_router
from app.api.db import router as db_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# 配置 CORS，允许前端本地开发调通
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(db_router, prefix="/api/db", tags=["Database"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up App and initializing databases...")
    await init_db()

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}
