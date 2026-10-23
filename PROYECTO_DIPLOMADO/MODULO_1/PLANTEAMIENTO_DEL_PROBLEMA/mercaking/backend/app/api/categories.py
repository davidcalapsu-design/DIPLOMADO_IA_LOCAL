"""Categories router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Category
from app.schemas.schemas import CategoryCreate, CategoryOut
import uuid

router = APIRouter()

@router.get("/", response_model=list[CategoryOut])
def list_categories(tenant_id: str = Query(...), db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.tenant_id == tenant_id, Category.is_active == True).all()

@router.post("/", response_model=CategoryOut)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    c = Category(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db)):
    c = db.query(Category).filter(Category.id == category_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    c.is_active = False
    db.commit()
    return {"ok": True}
