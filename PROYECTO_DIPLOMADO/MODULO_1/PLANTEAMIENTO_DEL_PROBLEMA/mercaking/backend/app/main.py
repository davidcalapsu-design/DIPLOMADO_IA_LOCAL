from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.api import auth, tenants, categories, suppliers, products, inventory, sales, dashboard, ai, superadmin

app = FastAPI(title="MercaKing API", version="0.1.0", description="API REST para MercaKing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/api/tenants", tags=["tenants"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(suppliers.router, prefix="/api/suppliers", tags=["suppliers"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(sales.router, prefix="/api/sales", tags=["sales"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(superadmin.router, prefix="/api/superadmin", tags=["superadmin"])


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": "0.1.0"}
