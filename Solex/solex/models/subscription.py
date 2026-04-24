import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

SUBSCRIPTION_STATUSES = ("active", "paused", "cancelled", "past_due")

class Subscription(BaseModel):
    __tablename__ = "subscriptions"
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False,
    )
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    cadence_days: Mapped[int] = mapped_column(Integer, nullable=False)
    square_card_id: Mapped[str] = mapped_column(String(120), nullable=False)
    next_charge_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    paused_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_charged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    charges: Mapped[list["SubscriptionCharge"]] = relationship(
        back_populates="subscription", cascade="all, delete-orphan",
    )
    __table_args__ = (
        Index("ix_subs_status", "status"),
        Index("ix_subs_next_charge", "next_charge_at"),
    )

class SubscriptionCharge(BaseModel):
    __tablename__ = "subscription_charges"
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False,
    )
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True,
    )
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    succeeded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    subscription: Mapped[Subscription] = relationship(back_populates="charges")
