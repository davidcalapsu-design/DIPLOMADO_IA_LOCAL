"""Tenants router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Tenant
from app.schemas.schemas import TenantCreate, TenantOut
import uuid

router = APIRouter()

@router.get("/", response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).filter(Tenant.is_active == True).all()

@router.get("/{tenant_id}", response_model=TenantOut)
def get_tenant(tenant_id: str, db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant no encontrado")
    return t

@router.post("/", response_model=TenantOut)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    t = Tenant(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t
