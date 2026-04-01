"""Strategy model — the primary entity in VIVA.

Everything resolves to a strategy: signals feed strategies,
strategies generate trades, trades produce P&L, P&L flows to treasury.
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Enum, String, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from viva.extensions import db


class StrategyType(enum.Enum):
    LATENCY_ARB = "latency_arb"
    ORACLE_ARB = "oracle_arb"
    NEWS_DRIVEN = "news_driven"
    MARKET_MAKER = "market_maker"
    CROSS_VENUE_ARB = "cross_venue_arb"


class StrategyStatus(enum.Enum):
    PROPOSED = "proposed"           # Submitted for council review
    APPROVED = "approved"           # Council approved, not yet live
    PAPER_TRADING = "paper_trading" # Running in paper mode
    LIVE = "live"                   # Deployed with real capital
    PAUSED = "paused"               # Temporarily halted (manual or kill switch)
    KILLED = "killed"               # Permanently halted (drawdown or council decision)
    REJECTED = "rejected"           # Council rejected proposal


class Strategy(db.Model):
    """A trading strategy with council-approved risk envelope."""

    __tablename__ = "strategies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    strategy_type: Mapped[StrategyType] = mapped_column(
        Enum(StrategyType), nullable=False
    )
    status: Mapped[StrategyStatus] = mapped_column(
        Enum(StrategyStatus), default=StrategyStatus.PROPOSED
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Risk envelope — council-set parameters
    max_position_pct: Mapped[float] = mapped_column(
        Float, default=0.30, doc="Max % of deployed capital this strategy can hold"
    )
    kill_switch_pct: Mapped[float] = mapped_column(
        Float, default=0.15, doc="Drawdown % that triggers automatic halt"
    )
    max_daily_trades: Mapped[int | None] = mapped_column(nullable=True)

    # Performance tracking
    total_trades: Mapped[int] = mapped_column(default=0)
    winning_trades: Mapped[int] = mapped_column(default=0)
    total_pnl_sats: Mapped[int] = mapped_column(default=0, doc="P&L in satoshis")
    peak_capital_sats: Mapped[int] = mapped_column(default=0)
    current_drawdown_pct: Mapped[float] = mapped_column(default=0.0)

    # Paper mode flag — overrides live execution
    paper_mode: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    approved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    killed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relationships
    trades: Mapped[list["Trade"]] = relationship(back_populates="strategy")
    positions: Mapped[list["Position"]] = relationship(back_populates="strategy")

    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return self.winning_trades / self.total_trades

    @property
    def is_active(self) -> bool:
        return self.status in (
            StrategyStatus.PAPER_TRADING,
            StrategyStatus.LIVE,
        )

    def __repr__(self) -> str:
        return f"<Strategy {self.name} [{self.strategy_type.value}] {self.status.value}>"
