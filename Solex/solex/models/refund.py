import uuid
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel


class Refund(BaseModel):
    __tablename__ = "refunds"
    # Nullable to support orphan-payment recovery (spec §4.10)
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=True,
    )
    square_refund_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(120), nullable=False)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
