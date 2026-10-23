"""AI assistant router (local-first)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import AuditLog
import uuid
import sys, os

# Make project root importable so `ai` package resolves
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai.agent.stock_agent import StockAgent

router = APIRouter()


class ChatRequest(BaseModel):
    tenant_id: str
    user_id: str = None
    question: str


@router.post("/chat")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    agent = StockAgent(db, payload.tenant_id)
    result = agent.answer(payload.question)

    # Log interaction as audit (AI_QUERY)
    db.add(AuditLog(
        id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        action="AI_QUERY",
        entity="ai",
        entity_id=None,
        details=f'{{"question": "{payload.question[:200]}", "used_llm": {str(result["used_llm"]).lower()}}}',
    ))
    db.commit()

    return {
        "question": result["question"],
        "answer": result["answer"],
        "used_llm": result["used_llm"],
        "ollama_available": result["ollama_available"],
        "context": {
            "matched_products": result["context"]["matched_products"],
            "low_stock": result["context"]["low_stock"],
            "sales_summary": result["context"]["sales_summary"],
        },
    }


@router.get("/health")
def ai_health():
    import requests
    url = __import__("os").getenv("OLLAMA_URL", "http://localhost:11434")
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        return {"ollama_available": r.status_code == 200, "url": url}
    except Exception:
        return {"ollama_available": False, "url": url}
