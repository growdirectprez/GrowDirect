import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

ORDER_STATUSES = ("pending", "paid", "shipped", "delivered",
                  "refunded", "partially_refunded", "cancelled", "failed")


class Order(BaseModel):
    __tablename__ = "orders"
    public_token: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    customer_email: Mapped[str] = mapped_column(String(254), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    shipping_address_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    billing_address_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    subtotal_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    tax_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    shipping_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
    square_order_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    square_payment_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    autoship: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    autoship_subscription_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fulfilled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    tracking_number: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    notes: Mapped[list["OrderNote"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    __table_args__ = (
        Index("ix_orders_status", "status"),
        Index("ix_orders_placed_at", "placed_at"),
        Index("ix_orders_scenario_tag", "scenario_tag"),
    )


class OrderItem(BaseModel):
    __tablename__ = "order_items"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True,
    )
    sku_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)
    name_snapshot: Mapped[str] = mapped_column(String(240), nullable=False)
    image_path_snapshot: Mapped[str] = mapped_column(String(400), default="", nullable=False)
    price_snapshot_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    line_total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped["Order"] = relationship(back_populates="items")


class OrderNote(BaseModel):
    __tablename__ = "order_notes"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    internal: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped["Order"] = relationship(back_populates="notes")
