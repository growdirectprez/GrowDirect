from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Product
from solex.services.square_client import SquareClient


class CatalogSyncService:
    def __init__(self, session: Session, square: SquareClient):
        self.session = session
        self.square = square

    def sync_all(self) -> dict:
        products = self.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        summary = {"synced": 0, "errored": 0}
        for p in products:
            try:
                obj = self.square.upsert_catalog_item(
                    name=p.name, description=p.description,
                    sku=p.sku, price_cents=p.price_cents,
                    square_object_id=p.square_catalog_object_id,
                )
                if not p.square_catalog_object_id and obj.get("id"):
                    p.square_catalog_object_id = obj["id"]
                summary["synced"] += 1
            except Exception:
                summary["errored"] += 1
        self.session.commit()
        return summary
