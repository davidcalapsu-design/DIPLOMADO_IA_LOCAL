"""Tests for product isolation between tenants."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.seed import seed_two_tenants, TENANT_A, TENANT_B


def test_products_isolated_by_tenant(client, db):
    seed_two_tenants(db)
    res_a = client.get(f"/api/products/?tenant_id={TENANT_A}")
    res_b = client.get(f"/api/products/?tenant_id={TENANT_B}")
    assert res_a.status_code == 200
    assert res_b.status_code == 200
    names_a = [p["name"] for p in res_a.json()]
    names_b = [p["name"] for p in res_b.json()]
    assert "Leche A" in names_a
    assert "Leche A" not in names_b
    assert "Pan B" in names_b
    assert "Pan B" not in names_a


def test_create_product_requires_tenant(client, db):
    seed_two_tenants(db)
    payload = {"tenant_id": TENANT_A, "name": "Nuevo Prod", "sale_price": 1000, "current_stock": 5}
    res = client.post("/api/products/", json=payload)
    assert res.status_code == 200
    assert res.json()["tenant_id"] == TENANT_A
