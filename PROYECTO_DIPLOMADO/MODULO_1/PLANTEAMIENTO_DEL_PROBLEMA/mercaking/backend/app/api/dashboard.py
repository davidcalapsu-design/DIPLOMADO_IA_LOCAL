"""Dashboard router."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.models import Product, Sale, Supplier
from app.schemas.schemas import DashboardMetrics

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
def metrics(tenant_id: str = Query(...), db: Session = Depends(get_db)):
    active_products = db.query(Product).filter(Product.tenant_id == tenant_id, Product.is_active == True).count()
    suppliers_count = db.query(Supplier).filter(Supplier.tenant_id == tenant_id, Supplier.is_active == True).count()
    low_stock_count = db.query(Product).filter(
        Product.tenant_id == tenant_id, Product.is_active == True,
        Product.current_stock <= Product.min_stock,
    ).count()

    today = datetime.utcnow().date()
    today_sales = db.query(Sale).filter(
        Sale.tenant_id == tenant_id,
        Sale.created_at >= datetime(today.year, today.month, today.day),
    ).all()
    today_sales_total = float(sum(s.total for s in today_sales))
    today_sales_count = len(today_sales)

    return DashboardMetrics(
        active_products=active_products,
        today_sales_total=today_sales_total,
        today_sales_count=today_sales_count,
        low_stock_count=low_stock_count,
        suppliers_count=suppliers_count,
    )
