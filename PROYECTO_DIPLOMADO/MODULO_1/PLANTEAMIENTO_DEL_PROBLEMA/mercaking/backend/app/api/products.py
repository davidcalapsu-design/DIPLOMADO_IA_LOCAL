"""Products router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Product
from app.schemas.schemas import ProductCreate, ProductUpdate, ProductOut
import uuid

router = APIRouter()

@router.get("/", response_model=list[ProductOut])
def list_products(
    tenant_id: str = Query(...),
    q: str = Query(None),
    category_id: str = Query(None),
    low_stock: bool = Query(False),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.tenant_id == tenant_id, Product.is_active == True)
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.barcode.ilike(like)) | (Product.sku.ilike(like)))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if low_stock:
        query = query.filter(Product.current_stock <= Product.min_stock)
    return query.all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    p = Product(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    p.is_active = False
    db.commit()
    return {"ok": True}
