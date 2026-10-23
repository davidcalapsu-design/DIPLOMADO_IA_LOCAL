"""Suppliers router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Supplier
from app.schemas.schemas import SupplierCreate, SupplierOut
import uuid

router = APIRouter()

@router.get("/", response_model=list[SupplierOut])
def list_suppliers(tenant_id: str = Query(...), db: Session = Depends(get_db)):
    return db.query(Supplier).filter(Supplier.tenant_id == tenant_id, Supplier.is_active == True).all()

@router.post("/", response_model=SupplierOut)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    s = Supplier(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: str, db: Session = Depends(get_db)):
    s = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    s.is_active = False
    db.commit()
    return {"ok": True}
