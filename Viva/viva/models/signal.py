"""Signal model — market data snapshots from signal layer."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from viva.extensions import db


class Signal(db.Model):
    """A market signal captured by the signal layer.

    Time-series data — pruned after retention window.
    """

    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    source: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="binance|coinbase|polymarket|kalshi|chainlink|news"
    )
    signal_type: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="price_tick|oracle_update|news_event|contract_update"
    )
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, doc="BTC-USD|ETH-USD|etc")
    value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, doc="0.0-1.0")

    # Raw payload for replay/debugging
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True, doc="JSON")

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Signal {self.source} {self.signal_type} {self.symbol}={self.value}>"
