"""Superadmin router (platform_admin only)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Tenant, Profile, Product, Sale, AuditLog

router = APIRouter()

@router.get("/stats")
def global_stats(db: Session = Depends(get_db)):
    return {
        "tenants": db.query(Tenant).count(),
        "active_tenants": db.query(Tenant).filter(Tenant.is_active == True).count(),
        "users": db.query(Profile).count(),
        "products": db.query(Product).count(),
        "sales": db.query(Sale).count(),
        "audit_logs": db.query(AuditLog).count(),
    }

@router.get("/tenants")
def list_all_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    out = []
    for t in tenants:
        out.append({
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "city": t.city,
            "is_active": t.is_active,
            "products": db.query(Product).filter(Product.tenant_id == t.id).count(),
            "sales": db.query(Sale).filter(Sale.tenant_id == t.id).count(),
        })
    return out

@router.get("/audit-logs")
def audit_logs(tenant_id: str = Query(None), limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(AuditLog)
    if tenant_id:
        q = q.filter(AuditLog.tenant_id == tenant_id)
    logs = q.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [
        {"id": l.id, "tenant_id": l.tenant_id, "user_id": l.user_id, "action": l.action,
         "entity": l.entity, "details": l.details, "created_at": l.created_at} for l in logs
    ]

@router.patch("/tenants/{tenant_id}/toggle")
def toggle_tenant(tenant_id: str, db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant no encontrado")
    t.is_active = not t.is_active
    db.commit()
    return {"id": t.id, "is_active": t.is_active}
