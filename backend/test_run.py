import asyncio
import os
os.environ["SESSION_DB_PATH"] = "data/test_db_manual.db"

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.database import init_db

async def run_tests():
    print("Initialising test DB...")
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("Testing POST /api/sessions")
        resp = await client.post("/api/sessions", json={"title": "Manual Test Session"})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        print("Created:", data)
        s_id = data["id"]
        
        print("Testing GET /api/sessions")
        resp = await client.get("/api/sessions")
        assert resp.status_code == 200, resp.text
        print("Sessions:", len(resp.json()))
        
        print(f"Testing GET /api/sessions/{s_id}")
        resp = await client.get(f"/api/sessions/{s_id}")
        assert resp.status_code == 200, resp.text
        print("Detail:", resp.json()["title"])
        
        print("Testing PUT /api/sessions/{id}/title")
        resp = await client.put(f"/api/sessions/{s_id}/title?title=Updated+Title")
        assert resp.status_code == 200, resp.text
        
        resp = await client.get(f"/api/sessions/{s_id}")
        print("Updated Title:", resp.json()["title"])
        
        print(f"Testing DELETE /api/sessions/{s_id}")
        resp = await client.delete(f"/api/sessions/{s_id}")
        assert resp.status_code == 200, resp.text
        
        resp = await client.get(f"/api/sessions/{s_id}")
        assert resp.status_code == 404
        print("Delete verified.")
        
        print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(run_tests())
