"""Seed helpers for tests."""
import uuid
from app.models.models import Tenant, Category, Product

TENANT_A = "aaaaaaaa-0000-0000-0000-000000000001"
TENANT_B = "bbbbbbbb-0000-0000-0000-000000000002"


def seed_two_tenants(db):
    for tid, name, slug, city in [(TENANT_A, "Tienda A", "tienda-a", "Bogotá"),
                                   (TENANT_B, "Tienda B", "tienda-b", "Medellín")]:
        db.add(Tenant(id=tid, name=name, slug=slug, city=city))
    db.commit()

    # categories
    ca = uuid.uuid4().__str__()
    cb = uuid.uuid4().__str__()
    db.add(Category(id=ca, tenant_id=TENANT_A, name="Lácteos"))
    db.add(Category(id=cb, tenant_id=TENANT_B, name="Panadería"))
    db.commit()

    # products
    db.add(Product(id=str(uuid.uuid4()), tenant_id=TENANT_A, category_id=ca, name="Leche A", sale_price=4200, current_stock=10, min_stock=5))
    db.add(Product(id=str(uuid.uuid4()), tenant_id=TENANT_B, category_id=cb, name="Pan B", sale_price=3000, current_stock=20, min_stock=5))
    db.commit()
    return TENANT_A, TENANT_B
