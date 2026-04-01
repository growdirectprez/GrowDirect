"""Abstract base strategy — all VIVA strategies implement this interface."""

import abc
import logging
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class TradeSignal:
    """A signal that a strategy wants to execute a trade."""

    strategy_id: str
    venue: str
    market_id: str
    side: str  # buy | sell
    size_sats: int
    entry_price: float
    confidence: float  # 0.0 - 1.0
    reasoning: str
    timestamp: datetime


@dataclass
class RiskEnvelope:
    """Council-approved risk parameters for a strategy."""

    max_position_pct: float  # Max % of deployed capital
    kill_switch_pct: float  # Drawdown that triggers halt
    max_daily_trades: int | None
    paper_mode: bool


class BaseStrategy(abc.ABC):
    """Abstract strategy interface.

    Every strategy module implements:
    - evaluate() — assess current market state, return TradeSignal or None
    - should_close() — check if open position should be closed
    - name — human-readable strategy name
    """

    def __init__(self, risk_envelope: RiskEnvelope):
        self.risk_envelope = risk_envelope
        self.trades_today = 0
        self._last_reset = datetime.now(timezone.utc).date()

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable strategy name."""
        ...

    @abc.abstractmethod
    def evaluate(self, market_state: dict) -> TradeSignal | None:
        """Evaluate current market state and return a trade signal.

        Args:
            market_state: Dict with keys depending on strategy type.
                Latency arb: cex_price, prediction_price, spread, latency_ms
                Oracle arb: oracle_price, market_price, update_age_ms
                News: event_text, current_odds, pre_event_odds
                Market maker: bid, ask, spread, depth

        Returns:
            TradeSignal if conditions met, None otherwise.
        """
        ...

    @abc.abstractmethod
    def should_close(self, position: dict, market_state: dict) -> bool:
        """Check if an open position should be closed.

        Args:
            position: Current position details.
            market_state: Current market state.

        Returns:
            True if position should be closed.
        """
        ...

    def can_trade(self) -> bool:
        """Check if strategy is within daily trade limits."""
        today = datetime.now(timezone.utc).date()
        if today != self._last_reset:
            self.trades_today = 0
            self._last_reset = today

        if self.risk_envelope.max_daily_trades is not None:
            return self.trades_today < self.risk_envelope.max_daily_trades
        return True

    def record_trade(self) -> None:
        """Increment daily trade counter."""
        self.trades_today += 1
