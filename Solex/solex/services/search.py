# solex/services/search.py
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from solex.models import Product


class SearchService:
    def __init__(self, session: Session):
        self.session = session

    def search(self, query: str, limit: int = 20) -> list[Product]:
        """Full-text search over products using the tsvector index.

        Falls back to an empty list if the query is blank.
        """
        query = query.strip()
        if not query:
            return []

        # Use plainto_tsquery so raw user input is safe (no tsquery syntax errors)
        stmt = (
            select(Product)
            .where(
                Product.active == True,
                Product.search_tsv.op("@@")(
                    text("plainto_tsquery('english', :q)")
                ),
            )
            .order_by(
                text(
                    "ts_rank(products.search_tsv, plainto_tsquery('english', :q)) DESC"
                )
            )
            .limit(limit)
        )
        rows = self.session.execute(stmt, {"q": query}).scalars().all()
        return list(rows)
