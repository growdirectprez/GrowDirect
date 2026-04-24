from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from solex.models import Product, Category

class CatalogService:
    def __init__(self, session: Session):
        self.session = session

    def list_products(self, category_slug: str | None = None, active_only: bool = True):
        q = select(Product).options(selectinload(Product.category))
        if active_only:
            q = q.where(Product.active == True)
        if category_slug:
            q = q.join(Category).where(Category.slug == category_slug)
        return self.session.execute(q.order_by(Product.name)).scalars().all()

    def get_product(self, slug: str) -> Product | None:
        return self.session.execute(
            select(Product).where(Product.slug == slug)
        ).scalar_one_or_none()

    def get_product_by_id(self, product_id):
        return self.session.get(Product, product_id)

    def list_categories(self):
        return self.session.execute(
            select(Category).order_by(Category.sort, Category.name)
        ).scalars().all()
