# MercaKing — Plataforma SaaS Multi-inquilino con IA Local para Minimercados

## Descripción
Plataforma SaaS multi-inquilino para minimercados colombianos: inventarios, ventas (POS), proveedores, reportes y asistente de IA local.

## Stack
- **Backend:** Python (FastAPI) + SQLAlchemy + MySQL
- **Frontend:** Python (Flask + Jinja2)
- **BD:** MySQL (administrada con phpMyAdmin)
- **IA (Fase 3):** Ollama + RAG + OCR (local-first)

## Estructura
```
mercaking/
├── backend/     # API REST FastAPI
├── database/    # SQL para phpMyAdmin
├── ai/          # Módulo IA (Fase 3)
├── frontend/    # Web Flask + Jinja2
├── docs/        # Plan y documentación
└── PLAN_MERCAKING.md
```

## Cómo correr (desarrollo)

### 1. Base de datos
1. Abre phpMyAdmin.
2. Crea la BD `mercaking` (utf8mb4).
3. Importa `database/schema.sql` y luego `database/seed.sql`.

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API disponible en http://localhost:8000 (docs en /docs).

### 3. Frontend (Flask)
```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Web disponible en http://localhost:5000.

## Plan
Ver `PLAN_MERCAKING.md` y `docs/`.
