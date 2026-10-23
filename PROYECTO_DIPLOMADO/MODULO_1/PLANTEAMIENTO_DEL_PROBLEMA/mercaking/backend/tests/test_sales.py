"""Tests for POS sale processing."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
from tests.seed import seed_two_tenants, TENANT_A
from app.models.models import Product


def test_pos_sale_discounts_stock(client, db):
    seed_two_tenants(db)
    prod = db.query(Product).filter(Product.tenant_id == TENANT_A).first()
    initial_stock = float(prod.current_stock)
    payload = {
        "tenant_id": TENANT_A,
        "payment_method": "cash",
        "amount_paid": 5000,
        "items": [{"product_id": prod.id, "quantity": 2, "unit_price": 4200}],
    }
    res = client.post("/api/sales/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["sale_number"].startswith("VTA-")
    # stock discounted
    prod2 = db.query(Product).filter(Product.id == prod.id).first()
    assert float(prod2.current_stock) == initial_stock - 2


def test_pos_sale_insufficient_stock(client, db):
    seed_two_tenants(db)
    prod = db.query(Product).filter(Product.tenant_id == TENANT_A).first()
    payload = {
        "tenant_id": TENANT_A,
        "payment_method": "cash",
        "amount_paid": 100000,
        "items": [{"product_id": prod.id, "quantity": 9999, "unit_price": 4200}],
    }
    res = client.post("/api/sales/", json=payload)
    assert res.status_code == 400
