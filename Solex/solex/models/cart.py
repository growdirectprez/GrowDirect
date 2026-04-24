import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

if TYPE_CHECKING:
    from solex.models.customer import Customer


class Cart(BaseModel):
    __tablename__ = "carts"
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    session_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    applied_promo_code: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recovered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    abandonment_emailed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    lines: Mapped[list["CartLine"]] = relationship(back_populates="cart", cascade="all, delete-orphan")
    customer: Mapped[Optional["Customer"]] = relationship("Customer", foreign_keys=[customer_id])
    __table_args__ = (
        Index("ix_carts_session", "session_key"),
        Index("ix_carts_customer", "customer_id"),
    )


class CartLine(BaseModel):
    __tablename__ = "cart_lines"
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False,
    )
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price_snapshot_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    cart: Mapped["Cart"] = relationship(back_populates="lines")
