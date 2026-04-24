from pathlib import Path
import shutil
import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Category, Product, Inventory

class CatalogImporter:
    def __init__(self, session: Session, catalog_root: Path, static_root: Path):
        self.session = session
        self.catalog_root = Path(catalog_root)
        self.static_root = Path(static_root)

    def import_from_yaml(self, yaml_path: Path) -> dict:
        data = yaml.safe_load(Path(yaml_path).read_text())
        counts = {"categories": {"inserted": 0, "updated": 0},
                  "products":   {"inserted": 0, "updated": 0}}

        slug_to_cat = {}
        for c in data.get("categories", []):
            cat = self.session.execute(
                select(Category).where(Category.slug == c["slug"])
            ).scalar_one_or_none()
            if cat is None:
                cat = Category(slug=c["slug"], name=c["name"], sort=c.get("sort", 0))
                self.session.add(cat)
                counts["categories"]["inserted"] += 1
            else:
                cat.name = c["name"]; cat.sort = c.get("sort", 0)
                counts["categories"]["updated"] += 1
            slug_to_cat[c["slug"]] = cat
        self.session.flush()

        for p in data.get("products", []):
            prod = self.session.execute(
                select(Product).where(Product.sku == p["sku"])
            ).scalar_one_or_none()
            category = slug_to_cat.get(p.get("category_slug"))
            fields = dict(
                sku=p["sku"], slug=p["slug"], name=p["name"],
                description=p.get("description", ""),
                short_description=p.get("short_description", ""),
                price_cents=p["price_cents"],
                image_path=p.get("image_path", ""),
                category_id=(category.id if category else None),
                active=p.get("active", True),
                weight_grams=p.get("weight_grams", 0),
            )
            if prod is None:
                prod = Product(**fields)
                self.session.add(prod)
                counts["products"]["inserted"] += 1
            else:
                for k, v in fields.items():
                    setattr(prod, k, v)
                counts["products"]["updated"] += 1
            self.session.flush()

            inv = self.session.execute(
                select(Inventory).where(Inventory.product_id == prod.id)
            ).scalar_one_or_none()
            if inv is None:
                self.session.add(Inventory(product_id=prod.id, on_hand=p.get("starting_inventory", 0)))

            self._copy_image(p.get("image_path"))

        self.session.commit()
        return counts

    def _copy_image(self, rel_path: str | None):
        if not rel_path:
            return
        src = self.catalog_root / rel_path.replace("catalog/", "")
        dst = self.static_root / "catalog" / rel_path.replace("catalog/", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)
