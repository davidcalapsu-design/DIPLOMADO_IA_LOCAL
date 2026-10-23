"""Inventory router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app.core.database import get_db
from app.models.models import Product, InventoryMovement, AuditLog
from app.schemas.schemas import MovementCreate, MovementOut
import uuid

router = APIRouter()

@router.get("/movements", response_model=list[MovementOut])
def list_movements(tenant_id: str, product_id: str = None, db: Session = Depends(get_db)):
    q = db.query(InventoryMovement).filter(InventoryMovement.tenant_id == tenant_id)
    if product_id:
        q = q.filter(InventoryMovement.product_id == product_id)
    return q.order_by(InventoryMovement.created_at.desc()).all()

@router.post("/movement", response_model=MovementOut)
def register_movement(payload: MovementCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == payload.product_id, Product.tenant_id == payload.tenant_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado en este minimercado")
    current = Decimal(str(product.current_stock))
    mtype = payload.movement_type
    qty = payload.quantity
    if mtype == "entry":
        new_stock = current + qty
    elif mtype == "exit":
        if current < qty:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente. Disponible: {current}, solicitado: {qty}")
        new_stock = current - qty
    elif mtype == "adjustment":
        new_stock = qty
        if new_stock < 0:
            raise HTTPException(status_code=400, detail="El stock resultante no puede ser negativo")
    else:
        raise HTTPException(status_code=400, detail="Tipo de movimiento no válido")

    product.current_stock = new_stock
    movement = InventoryMovement(
        id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        product_id=payload.product_id,
        user_id=payload.user_id,
        movement_type=mtype,
        quantity=abs(new_stock - current),
        previous_stock=current,
        new_stock=new_stock,
        reason=payload.reason,
    )
    db.add(movement)
    db.add(AuditLog(
        id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        action=f"INVENTORY_{mtype.upper()}",
        entity="products",
        entity_id=payload.product_id,
        details=f'{{"previous": {current}, "new": {new_stock}, "reason": "{payload.reason}"}}',
    ))
    db.commit()
    db.refresh(movement)
    return movement

@router.get("/low-stock")
def low_stock(tenant_id: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.is_active == True,
        Product.current_stock <= Product.min_stock,
    ).all()
    return [{"id": p.id, "name": p.name, "current_stock": float(p.current_stock), "min_stock": float(p.min_stock)} for p in products]
