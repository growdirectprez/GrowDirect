"""Kill switch — safety-critical, automatic halt.

THIS FILE IS PROTECTED. Changes require council review.

The kill switch operates independently of governance. It does not wait
for a council vote. When triggered, it:
1. Closes all open positions at market price
2. Pauses all active strategies
3. Logs a CouncilVerdict with type EMERGENCY_HALT
4. Sends alert to Jeffe
5. Refuses to re-enable without explicit manual override

Kill switch thresholds are set per-strategy (default -15%) and
portfolio-wide (default -15% of total deployed capital).
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class KillSwitchConfig:
    """Kill switch parameters — loaded from app config."""

    per_strategy_drawdown_pct: float = 0.15  # -15%
    portfolio_drawdown_pct: float = 0.15  # -15%
    correlation_threshold: float = 0.70  # Shut down correlated strategies
    max_single_loss_pct: float = 0.05  # -5% single trade = immediate review


@dataclass
class KillSwitchEvent:
    """Record of a kill switch activation."""

    triggered_at: datetime
    trigger_type: str  # strategy_drawdown | portfolio_drawdown | correlation | single_loss
    strategy_id: str | None
    drawdown_pct: float
    message: str


def check_strategy_drawdown(
    current_drawdown_pct: float,
    threshold: float,
    strategy_id: str,
    strategy_name: str,
) -> KillSwitchEvent | None:
    """Check if a strategy has breached its drawdown limit.

    Returns KillSwitchEvent if triggered, None otherwise.
    """
    if abs(current_drawdown_pct) >= threshold:
        event = KillSwitchEvent(
            triggered_at=datetime.now(timezone.utc),
            trigger_type="strategy_drawdown",
            strategy_id=strategy_id,
            drawdown_pct=current_drawdown_pct,
            message=(
                f"KILL SWITCH: Strategy '{strategy_name}' hit "
                f"{current_drawdown_pct:.1%} drawdown (limit: {threshold:.1%}). "
                f"All positions closed. Manual override required to restart."
            ),
        )
        logger.critical(event.message)
        return event
    return None


def check_portfolio_drawdown(
    total_deployed_sats: int,
    current_value_sats: int,
    threshold: float,
) -> KillSwitchEvent | None:
    """Check if total portfolio has breached drawdown limit."""
    if total_deployed_sats == 0:
        return None

    drawdown = (total_deployed_sats - current_value_sats) / total_deployed_sats

    if drawdown >= threshold:
        event = KillSwitchEvent(
            triggered_at=datetime.now(timezone.utc),
            trigger_type="portfolio_drawdown",
            strategy_id=None,
            drawdown_pct=drawdown,
            message=(
                f"KILL SWITCH: Portfolio drawdown {drawdown:.1%} "
                f"(limit: {threshold:.1%}). ALL strategies halted. "
                f"Manual override required."
            ),
        )
        logger.critical(event.message)
        return event
    return None


def check_correlation(
    strategy_a_losses: list[float],
    strategy_b_losses: list[float],
    threshold: float,
    strategy_a_name: str,
    strategy_b_name: str,
) -> KillSwitchEvent | None:
    """Check if two strategies have correlated losses.

    If correlation > threshold, the younger strategy is shut down.
    """
    if len(strategy_a_losses) < 10 or len(strategy_b_losses) < 10:
        return None  # Not enough data

    # Simple Pearson correlation on loss sequences
    n = min(len(strategy_a_losses), len(strategy_b_losses))
    a = strategy_a_losses[-n:]
    b = strategy_b_losses[-n:]

    mean_a = sum(a) / n
    mean_b = sum(b) / n

    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n)) / n
    std_a = (sum((x - mean_a) ** 2 for x in a) / n) ** 0.5
    std_b = (sum((x - mean_b) ** 2 for x in b) / n) ** 0.5

    if std_a == 0 or std_b == 0:
        return None

    correlation = cov / (std_a * std_b)

    if correlation > threshold:
        event = KillSwitchEvent(
            triggered_at=datetime.now(timezone.utc),
            trigger_type="correlation",
            strategy_id=None,
            drawdown_pct=correlation,
            message=(
                f"KILL SWITCH: Strategies '{strategy_a_name}' and "
                f"'{strategy_b_name}' show {correlation:.2f} loss correlation "
                f"(limit: {threshold:.2f}). Younger strategy halted."
            ),
        )
        logger.critical(event.message)
        return event
    return None
