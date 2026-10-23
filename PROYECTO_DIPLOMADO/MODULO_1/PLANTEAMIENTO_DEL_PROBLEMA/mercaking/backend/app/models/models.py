"""SQLAlchemy models for MercaKing (MySQL)."""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, DECIMAL, Text, Enum, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def new_uuid() -> str:
    return str(uuid.uuid4())


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String(36), primary_key=True, default=new_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    nit = Column(String(50))
    phone = Column(String(50))
    email = Column(String(150))
    address = Column(String(255))
    city = Column(String(100), default="Bogotá")
    currency = Column(String(10), default="COP")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("Category", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String(36), primary_key=True, default=new_uuid)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    avatar_url = Column(Text)
    system_role = Column(
        Enum("platform_admin", "store_owner", "store_admin", "cashier", "inventory_manager"),
        default="cashier", nullable=False,
    )
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserTenant(Base):
    __tablename__ = "user_tenants"
    id = Column(String(36), primary_key=True, default=new_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    role = Column(
        Enum("platform_admin", "store_owner", "store_admin", "cashier", "inventory_manager"),
        default="cashier", nullable=False,
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="categories")
    products = relationship("Product", back_populates="category")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    nit_rut = Column(String(50))
    phone = Column(String(50))
    email = Column(String(150))
    address = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"))
    supplier_id = Column(String(36), ForeignKey("suppliers.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    barcode = Column(String(100))
    sku = Column(String(100))
    description = Column(Text)
    purchase_price = Column(DECIMAL(12, 2), default=0.00)
    sale_price = Column(DECIMAL(12, 2), default=0.00)
    current_stock = Column(DECIMAL(12, 2), default=0.00)
    min_stock = Column(DECIMAL(12, 2), default=5.00)
    unit_measure = Column(String(50), default="unidad")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="products")
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="SET NULL"))
    movement_type = Column(Enum("entry", "exit", "adjustment", "sale"), nullable=False)
    quantity = Column(DECIMAL(12, 2), nullable=False)
    previous_stock = Column(DECIMAL(12, 2), nullable=False)
    new_stock = Column(DECIMAL(12, 2), nullable=False)
    reason = Column(String(255), nullable=False)
    reference_id = Column(String(36))
    created_at = Column(DateTime, default=datetime.utcnow)


class Sale(Base):
    __tablename__ = "sales"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="SET NULL"))
    sale_number = Column(String(50), nullable=False)
    customer_name = Column(String(150), default="Consumidor Final")
    customer_doc = Column(String(50))
    subtotal = Column(DECIMAL(12, 2), default=0.00)
    tax = Column(DECIMAL(12, 2), default=0.00)
    discount = Column(DECIMAL(12, 2), default=0.00)
    total = Column(DECIMAL(12, 2), default=0.00)
    payment_method = Column(Enum("cash", "card", "transfer", "other"), default="cash")
    amount_paid = Column(DECIMAL(12, 2), default=0.00)
    change_given = Column(DECIMAL(12, 2), default=0.00)
    status = Column(Enum("completed", "cancelled"), default="completed")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"
    id = Column(String(36), primary_key=True, default=new_uuid)
    sale_id = Column(String(36), ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(DECIMAL(12, 2), nullable=False)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=new_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"))
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    entity_id = Column(String(36))
    details = Column(Text)  # JSON as text for simplicity
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
