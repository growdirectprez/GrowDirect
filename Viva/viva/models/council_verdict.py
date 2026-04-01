"""CouncilVerdict model — append-only audit trail of council decisions."""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Enum, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from viva.extensions import db


class VerdictType(enum.Enum):
    STRATEGY_APPROVAL = "strategy_approval"
    STRATEGY_REJECTION = "strategy_rejection"
    RISK_ENVELOPE_CHANGE = "risk_envelope_change"
    EMERGENCY_HALT = "emergency_halt"
    PERFORMANCE_REVIEW = "performance_review"
    PHASE_GATE = "phase_gate"


class CouncilVerdict(db.Model):
    """Append-only record of a council decision.

    Never updated or deleted. The audit trail is permanent.
    """

    __tablename__ = "council_verdicts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("strategies.id"), nullable=True,
        doc="NULL for portfolio-level decisions"
    )

    verdict_type: Mapped[VerdictType] = mapped_column(
        Enum(VerdictType), nullable=False
    )
    decision: Mapped[str] = mapped_column(
        String(50), nullable=False, doc="approved|rejected|modified|halted"
    )

    # Council deliberation record
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    delegate_count: Mapped[int] = mapped_column(default=5)
    consensus: Mapped[str] = mapped_column(
        String(20), nullable=False, doc="5-0|4-1|3-2|etc"
    )

    # Risk parameters at time of decision
    risk_snapshot: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="JSON of risk state at decision time"
    )

    # Timestamps — created only, never updated
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<CouncilVerdict {self.verdict_type.value} {self.decision} ({self.consensus})>"
