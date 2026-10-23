"""Tests for AI assistant tenant isolation."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.seed import seed_two_tenants, TENANT_A, TENANT_B


def test_ai_chat_returns_answer(client, db):
    seed_two_tenants(db)
    res = client.post("/api/ai/chat", json={"tenant_id": TENANT_A, "question": "stock bajo"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert data["ollama_available"] in (True, False)


def test_ai_chat_empty_question_rejected(client, db):
    seed_two_tenants(db)
    res = client.post("/api/ai/chat", json={"tenant_id": TENANT_A, "question": "   "})
    assert res.status_code == 400


def test_ai_isolation_no_cross_tenant_data(client, db):
    seed_two_tenants(db)
    # Tenant A's AI should not mention Tenant B's product
    res = client.post("/api/ai/chat", json={"tenant_id": TENANT_A, "question": "pan"})
    data = res.json()
    assert "Pan B" not in data["answer"]
    assert "Pan B" not in str(data["context"])
