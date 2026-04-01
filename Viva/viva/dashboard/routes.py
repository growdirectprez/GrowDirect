"""VIVA dashboard — read-only view of portfolio state, strategies, P&L."""

from flask import Blueprint, jsonify
from flask_login import login_required

from viva.extensions import db
from viva.models.strategy import Strategy, StrategyStatus
from viva.models.trade import Trade, TradeOutcome
from viva.models.position import Position

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def overview():
    """Portfolio overview — strategies, positions, P&L summary."""
    strategies = db.session.query(Strategy).filter(
        Strategy.status.in_([
            StrategyStatus.PAPER_TRADING,
            StrategyStatus.LIVE,
            StrategyStatus.PAUSED,
        ])
    ).all()

    open_positions = db.session.query(Position).count()

    total_trades = db.session.query(Trade).count()
    winning_trades = db.session.query(Trade).filter(
        Trade.outcome == TradeOutcome.WIN
    ).count()

    total_pnl = db.session.query(
        db.func.coalesce(db.func.sum(Trade.pnl_sats), 0)
    ).scalar()

    return jsonify({
        "phase": "research",  # Read from config in production
        "strategies": [
            {
                "id": str(s.id),
                "name": s.name,
                "type": s.strategy_type.value,
                "status": s.status.value,
                "win_rate": s.win_rate,
                "total_trades": s.total_trades,
                "pnl_sats": s.total_pnl_sats,
                "paper_mode": s.paper_mode,
            }
            for s in strategies
        ],
        "portfolio": {
            "open_positions": open_positions,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "win_rate": winning_trades / total_trades if total_trades > 0 else 0,
            "total_pnl_sats": total_pnl,
        },
    })
