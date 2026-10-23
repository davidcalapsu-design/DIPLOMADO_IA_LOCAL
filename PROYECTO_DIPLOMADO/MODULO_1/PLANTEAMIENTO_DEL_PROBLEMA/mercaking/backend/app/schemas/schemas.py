"""Pydantic schemas for MercaKing."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ---------- Tenant ----------
class TenantBase(BaseModel):
    name: str
    slug: str
    nit: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = "Bogotá"
    currency: Optional[str] = "COP"
    is_active: bool = True

class TenantCreate(TenantBase):
    pass

class TenantOut(TenantBase):
    id: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Profile / Auth ----------
class ProfileBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    system_role: str = "cashier"
    is_active: bool = True

class ProfileCreate(ProfileBase):
    password: str
    tenant_id: Optional[str] = None

class ProfileOut(ProfileBase):
    id: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: ProfileOut


# ---------- Category ----------
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    tenant_id: str

class CategoryOut(CategoryBase):
    id: str
    tenant_id: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Supplier ----------
class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    nit_rut: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    tenant_id: str

class SupplierOut(SupplierBase):
    id: str
    tenant_id: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Product ----------
class ProductBase(BaseModel):
    name: str
    barcode: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    purchase_price: Decimal = 0
    sale_price: Decimal = 0
    current_stock: Decimal = 0
    min_stock: Decimal = 5
    unit_measure: str = "unidad"
    is_active: bool = True

class ProductCreate(ProductBase):
    tenant_id: str
    category_id: Optional[str] = None
    supplier_id: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    supplier_id: Optional[str] = None
    purchase_price: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    current_stock: Optional[Decimal] = None
    min_stock: Optional[Decimal] = None
    unit_measure: Optional[str] = None
    is_active: Optional[bool] = None

class ProductOut(ProductBase):
    id: str
    tenant_id: str
    category_id: Optional[str] = None
    supplier_id: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Inventory Movement ----------
class MovementCreate(BaseModel):
    tenant_id: str
    product_id: str
    user_id: Optional[str] = None
    movement_type: str  # entry/exit/adjustment/sale
    quantity: Decimal
    reason: str

class MovementOut(BaseModel):
    id: str
    tenant_id: str
    product_id: str
    movement_type: str
    quantity: Decimal
    previous_stock: Decimal
    new_stock: Decimal
    reason: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Sale ----------
class SaleItemIn(BaseModel):
    product_id: str
    quantity: Decimal
    unit_price: Decimal

class SaleCreate(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    customer_name: Optional[str] = "Consumidor Final"
    customer_doc: Optional[str] = None
    payment_method: str = "cash"
    amount_paid: Decimal = 0
    notes: Optional[str] = None
    items: List[SaleItemIn]

class SaleItemOut(BaseModel):
    id: str
    product_id: str
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal
    class Config:
        from_attributes = True

class SaleOut(BaseModel):
    id: str
    tenant_id: str
    sale_number: str
    customer_name: str
    total: Decimal
    payment_method: str
    amount_paid: Decimal
    change_given: Decimal
    status: str
    created_at: Optional[datetime] = None
    items: List[SaleItemOut] = []
    class Config:
        from_attributes = True


# ---------- Dashboard ----------
class DashboardMetrics(BaseModel):
    active_products: int = 0
    today_sales_total: float = 0
    today_sales_count: int = 0
    low_stock_count: int = 0
    suppliers_count: int = 0
