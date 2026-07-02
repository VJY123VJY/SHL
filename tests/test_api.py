import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_chat_clarify_then_recommend():
    # vague -> clarifying question
    r = client.post("/chat", json={"messages": [{"role": "user", "content": "I need an assessment"}]})
    assert r.status_code == 200
    assert r.json()["recommendations"] == []

    # provide role+seniority -> get recommendations
    r2 = client.post("/chat", json={"messages": [{"role": "user", "content": "Hiring a Java developer. Mid-level."}]})
    assert r2.status_code == 200
    body = r2.json()
    assert "reply" in body
    assert isinstance(body["recommendations"], list)
