import uuid
from typing import Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(BaseModel):
    __tablename__ = "products"
    sku: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    compare_at_cents: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    image_path: Mapped[str] = mapped_column(String(400), default="", nullable=False)
    gallery_paths: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weight_grams: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dimensions_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    square_catalog_object_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    # search_tsv is populated by DB trigger (migration 0003) — read-only from SQLAlchemy's POV
    search_tsv: Mapped[Optional[str]] = mapped_column(TSVECTOR, nullable=True, deferred=True)
    category: Mapped[Optional[Category]] = relationship(back_populates="products")
    tags: Mapped[list["ProductTag"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_products_active", "active"),
    )


class ProductTag(BaseModel):
    __tablename__ = "product_tags"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    tag: Mapped[str] = mapped_column(String(80), nullable=False)
    product: Mapped[Product] = relationship(back_populates="tags")
