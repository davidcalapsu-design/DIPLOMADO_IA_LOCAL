"""RAG retriever: gathers tenant-scoped context for the AI assistant."""
from sqlalchemy.orm import Session
from app.models.models import Product, Supplier, Sale, Tenant
from decimal import Decimal


class TenantRetriever:
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    def _tenant(self):
        return self.db.query(Tenant).filter(Tenant.id == self.tenant_id).first()

    def search_products(self, query: str, limit: int = 8):
        q = f"%{query}%"
        return (
            self.db.query(Product)
            .filter(Product.tenant_id == self.tenant_id, Product.is_active == True)
            .filter((Product.name.ilike(q)) | (Product.barcode.ilike(q)) | (Product.sku.ilike(q)))
            .limit(limit)
            .all()
        )

    def low_stock(self, limit: int = 10):
        return (
            self.db.query(Product)
            .filter(Product.tenant_id == self.tenant_id, Product.is_active == True,
                    Product.current_stock <= Product.min_stock)
            .limit(limit)
            .all()
        )

    def all_products(self, limit: int = 50):
        return (
            self.db.query(Product)
            .filter(Product.tenant_id == self.tenant_id, Product.is_active == True)
            .limit(limit)
            .all()
        )

    def suppliers(self, limit: int = 20):
        from app.models.models import Supplier
        return (
            self.db.query(Supplier)
            .filter(Supplier.tenant_id == self.tenant_id, Supplier.is_active == True)
            .limit(limit)
            .all()
        )

    def sales_summary(self, days: int = 7):
        since = __import__("datetime").datetime.utcnow() - __import__("datetime").timedelta(days=days)
        sales = self.db.query(Sale).filter(Sale.tenant_id == self.tenant_id, Sale.created_at >= since).all()
        total = sum(float(s.total) for s in sales)
        return {"count": len(sales), "total": round(total, 2), "days": days}

    def retrieve(self, question: str) -> dict:
        """Return a context dict + a text block for the LLM prompt."""
        tenant = self._tenant()
        tenant_name = tenant.name if tenant else "tu minimercado"

        # Try keyword search first
        words = [w for w in question.lower().split() if len(w) > 3]
        matched = []
        for w in words:
            matched.extend(self.search_products(w, limit=5))
        # de-dup
        seen = set()
        uniq = []
        for p in matched:
            if p.id not in seen:
                seen.add(p.id)
                uniq.append(p)

        low = self.low_stock()
        suppliers = self.suppliers()
        summary = self.sales_summary()

        lines = [f"Minimercado: {tenant_name}", ""]
        if uniq:
            lines.append("Productos encontrados:")
            for p in uniq:
                lines.append(f"- {p.name} | stock: {p.current_stock} {p.unit_measure} | precio venta: {p.sale_price} | mínimo: {p.min_stock}")
        if low:
            lines.append("")
            lines.append("Productos con stock bajo:")
            for p in low:
                lines.append(f"- {p.name}: {p.current_stock} (mín {p.min_stock})")
        if suppliers:
            lines.append("")
            lines.append("Proveedores:")
            for s in suppliers[:5]:
                lines.append(f"- {s.name} ({s.phone or ''})")
        lines.append("")
        lines.append(f"Ventas últimos {summary['days']} días: {summary['count']} ventas, total {summary['total']}")

        context_text = "\n".join(lines)
        return {
            "tenant_name": tenant_name,
            "matched_products": [{"id": p.id, "name": p.name, "stock": float(p.current_stock), "price": float(p.sale_price)} for p in uniq],
            "low_stock": [{"id": p.id, "name": p.name, "stock": float(p.current_stock), "min": float(p.min_stock)} for p in low],
            "suppliers": [{"id": s.id, "name": s.name, "phone": s.phone} for s in suppliers],
            "sales_summary": summary,
            "context_text": context_text,
        }
