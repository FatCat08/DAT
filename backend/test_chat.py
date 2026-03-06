import asyncio
import os
os.environ["SESSION_DB_PATH"] = "data/test_db_sse.db"
os.environ["BUSINESS_DB_PATH"] = "test_sales.db"

import httpx
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.database import init_db

async def run_tests():
    print("Initialising test DB...")
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create a session
        resp = await client.post("/api/sessions", json={"title": "SSE Chat Test"})
        s_id = resp.json()["id"]
        
        # 2. Test normal conversation first
        print("\n=== Testing Normal Conversation ===")
        async with client.stream("POST", "/api/chat", json={"session_id": s_id, "message": "hello, who are you?"}) as response:
            async for line in response.aiter_lines():
                if line:
                    print(line)

        # 3. Test Data Query conversation
        print("\n=== Testing Data Query Conversation ===")
        async with client.stream("POST", "/api/chat", json={"session_id": s_id, "message": "请问 IT 部门总销售额是多少？"}) as response:
            async for line in response.aiter_lines():
                if line:
                    print(line)
        
        print("\nAll tests finished!")

if __name__ == "__main__":
    asyncio.run(run_tests())
