import httpx
import json

def test_chat():
    with httpx.Client(timeout=60.0) as client:
        # Create a session first to have a valid ID
        res = client.post("http://localhost:8000/api/sessions", json={"title": "Test Session"})
        session_id = res.json()["id"]
        
        print(f"Created Session: {session_id}")
        
        with client.stream("POST", "http://localhost:8000/api/chat", json={
            "session_id": session_id,
            "message": "帮我看一下 Q4 的销售额情况，画个图表"
        }) as response:
            with open("test_sse_output.txt", "w", encoding="utf-8") as f:
                for line in response.iter_lines():
                    if line:
                        f.write(line + "\n")

if __name__ == "__main__":
    test_chat()
