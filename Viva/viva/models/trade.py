"""Trade model — append-only record of every trade VIVA executes."""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Enum, String, Float, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from viva.extensions import db


class TradeSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"


class TradeOutcome(enum.Enum):
    WIN = "win"
    LOSS = "loss"
    BREAK_EVEN = "break_even"
    PENDING = "pending"


class Trade(db.Model):
    """Individual trade record — append-only audit trail."""

    __tablename__ = "trades"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("strategies.id"), nullable=False
    )

    # Trade details
    venue: Mapped[str] = mapped_column(String(100), nullable=False, doc="polymarket|kalshi|etc")
    market_id: Mapped[str] = mapped_column(String(500), nullable=False, doc="Contract/market identifier")
    side: Mapped[TradeSide] = mapped_column(Enum(TradeSide), nullable=False)
    size_sats: Mapped[int] = mapped_column(Integer, nullable=False, doc="Position size in satoshis")
    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Execution metadata
    signal_confidence: Mapped[float] = mapped_column(Float, nullable=False, doc="0.0-1.0 signal confidence at entry")
    execution_latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    slippage_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    fees_sats: Mapped[int] = mapped_column(Integer, default=0)

    # Outcome
    outcome: Mapped[TradeOutcome] = mapped_column(
        Enum(TradeOutcome), default=TradeOutcome.PENDING
    )
    pnl_sats: Mapped[int] = mapped_column(Integer, default=0)

    # Paper mode flag
    paper_mode: Mapped[bool] = mapped_column(Boolean, default=True)

    # Context — what the market looked like at entry
    market_context: Mapped[str | None] = mapped_column(Text, nullable=True, doc="JSON snapshot of market state at entry")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relationships
    strategy: Mapped["Strategy"] = relationship(back_populates="trades")

    def __repr__(self) -> str:
        return f"<Trade {self.side.value} {self.venue} pnl={self.pnl_sats}sat>"
