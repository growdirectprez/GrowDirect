import uuid
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel


class Inventory(BaseModel):
    __tablename__ = "inventories"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    on_hand: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class InventoryAdjustment(BaseModel):
    __tablename__ = "inventory_adjustments"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False,
    )
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(40), nullable=False)
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True,
    )
    refund_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("refunds.id", ondelete="SET NULL"), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    __table_args__ = (
        Index("ix_inv_adj_product", "product_id"),
        Index("ix_inv_adj_reason", "reason"),
    )
