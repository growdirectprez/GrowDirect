"""Position model — current open positions with mark-to-market."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from viva.extensions import db


class Position(db.Model):
    """An open position in a prediction market or trading venue."""

    __tablename__ = "positions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("strategies.id"), nullable=False
    )

    venue: Mapped[str] = mapped_column(String(100), nullable=False)
    market_id: Mapped[str] = mapped_column(String(500), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)  # buy|sell

    # Size and pricing
    size_sats: Mapped[int] = mapped_column(Integer, nullable=False)
    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    unrealized_pnl_sats: Mapped[int] = mapped_column(Integer, default=0)

    # Risk state
    exposure_pct: Mapped[float] = mapped_column(
        Float, default=0.0, doc="% of total deployed capital"
    )

    paper_mode: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    strategy: Mapped["Strategy"] = relationship(back_populates="positions")

    @property
    def is_profitable(self) -> bool:
        return self.unrealized_pnl_sats > 0

    def __repr__(self) -> str:
        return f"<Position {self.venue} {self.side} unrealized={self.unrealized_pnl_sats}sat>"
