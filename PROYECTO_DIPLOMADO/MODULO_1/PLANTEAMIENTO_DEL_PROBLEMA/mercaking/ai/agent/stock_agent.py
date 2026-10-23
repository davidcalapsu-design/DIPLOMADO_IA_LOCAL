"""Stock agent: read-only assistant for minimercado data (local-first)."""
import os
import requests
from ai.rag.retriever import TenantRetriever

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

SYSTEM_PROMPT = """Eres MercaKing, un asistente inteligente para minimercados.
Respondes ÚNICAMENTE con la información del CONTEXTO proporcionado sobre la tienda del usuario.
Si la pregunta no puede responderse con el contexto, responde exactamente: "No tengo esa información en tu tienda."
No inventes datos. No ejecutes acciones ni escrituras. Responde en español, breve y claro."""


class StockAgent:
    def __init__(self, db, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id
        self.retriever = TenantRetriever(db, tenant_id)

    def _ollama_available(self) -> bool:
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def _call_ollama(self, question: str, context: str) -> str:
        prompt = f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}\n\nRESPUESTA:"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {"temperature": 0.2},
        }
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("response", "").strip()

    def _rule_based(self, question: str, ctx: dict) -> str:
        q = question.lower()
        if "stock bajo" in q or "bajo stock" in q or "alerta" in q:
            items = ctx["low_stock"]
            if not items:
                return "No hay productos con stock bajo en este momento. 🎉"
            return "Productos con stock bajo:\n" + "\n".join(f"- {i['name']}: {i['stock']} (mín {i['min']})" for i in items)
        if "proveedor" in q:
            sups = ctx["suppliers"]
            if not sups:
                return "No tengo proveedores registrados en tu tienda."
            return "Proveedores:\n" + "\n".join(f"- {s['name']} ({s['phone'] or 'sin teléfono'})" for s in sups)
        if "venta" in q:
            s = ctx["sales_summary"]
            return f"En los últimos {s['days']} días: {s['count']} ventas, total {s['total']}."
        # product search
        if ctx["matched_products"]:
            return "Productos encontrados:\n" + "\n".join(
                f"- {p['name']}: stock {p['stock']}, precio {p['price']}" for p in ctx["matched_products"]
            )
        return "No tengo esa información en tu tienda."

    def answer(self, question: str) -> dict:
        ctx = self.retriever.retrieve(question)
        context_text = ctx["context_text"]
        used_llm = False
        try:
            if self._ollama_available():
                answer = self._call_ollama(question, context_text)
                used_llm = True
            else:
                answer = self._rule_based(question, ctx)
        except Exception as e:
            answer = self._rule_based(question, ctx)
            answer += f"\n\n(Nota: IA local no disponible: {e})"
        return {
            "question": question,
            "answer": answer,
            "context": ctx,
            "used_llm": used_llm,
            "ollama_available": self._ollama_available(),
        }
