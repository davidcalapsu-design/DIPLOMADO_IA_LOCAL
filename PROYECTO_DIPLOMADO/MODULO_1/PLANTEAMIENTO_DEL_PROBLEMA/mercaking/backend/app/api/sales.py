"""Sales / POS router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app.core.database import get_db
from app.models.models import Product, Sale, SaleItem, InventoryMovement, AuditLog
from app.schemas.schemas import SaleCreate, SaleOut, SaleItemOut
import uuid

router = APIRouter()

@router.post("/", response_model=SaleOut)
def process_sale(payload: SaleCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="La venta debe contener al menos un producto")

    # Validar productos y stock
    subtotal = Decimal("0")
    prod_map = {}
    for item in payload.items:
        p = db.query(Product).filter(Product.id == item.product_id, Product.tenant_id == payload.tenant_id, Product.is_active == True).first()
        if not p:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no existe o está inactivo")
        if Decimal(str(p.current_stock)) < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{p.name}'. Disponible: {p.current_stock}, solicitado: {item.quantity}")
        prod_map[item.product_id] = p
        subtotal += item.quantity * item.unit_price

    total = subtotal
    if payload.amount_paid < total and payload.payment_method == "cash":
        raise HTTPException(status_code=400, detail=f"Monto pagado ({payload.amount_paid}) menor al total ({total})")
    change = payload.amount_paid - total if payload.amount_paid >= total else Decimal("0")

    # Número de venta
    count = db.query(Sale).filter(Sale.tenant_id == payload.tenant_id).count()
    sale_number = f"VTA-{count + 1:06d}"

    sale = Sale(
        id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        sale_number=sale_number,
        customer_name=payload.customer_name or "Consumidor Final",
        customer_doc=payload.customer_doc,
        subtotal=subtotal,
        total=total,
        payment_method=payload.payment_method,
        amount_paid=payload.amount_paid,
        change_given=change,
        notes=payload.notes,
    )
    db.add(sale)
    db.flush()

    for item in payload.items:
        p = prod_map[item.product_id]
        prev_stock = Decimal(str(p.current_stock))
        db.add(SaleItem(
            id=str(uuid.uuid4()),
            sale_id=sale.id,
            tenant_id=payload.tenant_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price,
        ))
        p.current_stock = prev_stock - item.quantity
        db.add(InventoryMovement(
            id=str(uuid.uuid4()),
            tenant_id=payload.tenant_id,
            product_id=item.product_id,
            user_id=payload.user_id,
            movement_type="sale",
            quantity=item.quantity,
            previous_stock=prev_stock,
            new_stock=prev_stock - item.quantity,
            reason=f"Venta registrada #{sale_number}",
            reference_id=sale.id,
        ))

    db.add(AuditLog(
        id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        action="SALE_COMPLETED",
        entity="sales",
        entity_id=sale.id,
        details=f'{{"sale_number": "{sale_number}", "total": {total}, "items": {len(payload.items)}}}',
    ))
    db.commit()
    db.refresh(sale)

    items_out = [SaleItemOut.model_validate(i) for i in sale.items]
    return SaleOut(
        id=sale.id,
        tenant_id=sale.tenant_id,
        sale_number=sale.sale_number,
        customer_name=sale.customer_name,
        total=sale.total,
        payment_method=sale.payment_method,
        amount_paid=sale.amount_paid,
        change_given=sale.change_given,
        status=sale.status,
        created_at=sale.created_at,
        items=items_out,
    )

@router.get("/history", response_model=list[SaleOut])
def sales_history(tenant_id: str, limit: int = 50, db: Session = Depends(get_db)):
    sales = db.query(Sale).filter(Sale.tenant_id == tenant_id).order_by(Sale.created_at.desc()).limit(limit).all()
    out = []
    for s in sales:
        out.append(SaleOut(
            id=s.id,
            tenant_id=s.tenant_id,
            sale_number=s.sale_number,
            customer_name=s.customer_name,
            total=s.total,
            payment_method=s.payment_method,
            amount_paid=s.amount_paid,
            change_given=s.change_given,
            status=s.status,
            created_at=s.created_at,
            items=[SaleItemOut.model_validate(i) for i in s.items],
        ))
    return out
