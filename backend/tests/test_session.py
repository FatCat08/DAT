import pytest
from httpx import AsyncClient, ASGITransport
import os

from app.main import app

# We override the DB path for testing so it doesn't pollute real data
os.environ["SESSION_DB_PATH"] = "data/test_sessions.db"

@pytest.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# Ensure we hit the database startup logic
@pytest.fixture(autouse=True)
async def lifespan_mock():
    # FastAPI's lifespans aren't automatically triggered in AsyncClient without LifespanManager or explicit call.
    # But since we use @app.on_event("startup") in main.py, let's call it manually if needed, or rely on ASGITransport handling it if configured.
    from app.models.database import init_db
    import aiosqlite
    import asyncio
    
    # Initialize real tables onto the test DB
    await init_db()
    
    yield
    
    # Teardown logic
    if os.path.exists("data/test_sessions.db"):
        pass # we can remove it later, keeping for debugging

@pytest.mark.asyncio
async def test_create_session(async_client: AsyncClient):
    response = await async_client.post("/api/sessions", json={"title": "Test Chat"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data
    return data["id"]

@pytest.mark.asyncio
async def test_get_sessions(async_client: AsyncClient):
    # create at least one
    await async_client.post("/api/sessions", json={"title": "Chat 1"})
    
    response = await async_client.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_update_session_title(async_client: AsyncClient):
    # Create
    resp = await async_client.post("/api/sessions", json={"title": "Old Title"})
    s_id = resp.json()["id"]
    
    # Update
    update_resp = await async_client.put(f"/api/sessions/{s_id}/title?title=New+Title")
    assert update_resp.status_code == 200
    
    # Verify
    get_resp = await async_client.get(f"/api/sessions/{s_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "New Title"

@pytest.mark.asyncio
async def test_delete_session(async_client: AsyncClient):
    # Create
    resp = await async_client.post("/api/sessions", json={"title": "To Delete"})
    s_id = resp.json()["id"]
    
    # Delete
    del_resp = await async_client.delete(f"/api/sessions/{s_id}")
    assert del_resp.status_code == 200
    
    # Verify missing
    get_resp = await async_client.get(f"/api/sessions/{s_id}")
    assert get_resp.status_code == 404
