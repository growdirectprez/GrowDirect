"""Angel module — Lead pipeline model.

A lead is born when an APN changes status or a visitor engages with Angel.
Stages: identified → engaged → captured → contacted → showing → offer → escrow → closed → archived

Schema reference: docs/sdds/angel/data-platform.md §4.3

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real model is in ~/GrowDirect/Cove/cove/models/lead.py.
This file provided for scaffolding reference.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from angel import db


LEAD_STAGES = [
    "identified",   # APN-based signal (transfer, expiration, equity), no visitor interaction
    "engaged",      # Visitor started Angel conversation (3+ turns)
    "captured",     # Phone number collected via Angel widget
    "contacted",    # Angelique has called/texted back
    "showing",      # Property tour scheduled
    "offer",        # Offer submitted
    "escrow",       # Under contract
    "closed",       # Transaction closed
    "archived",     # Not pursuing, with reason
]


class Lead(db.Model):
    """A real estate lead tied to a parcel (APN). Tracks through pipeline to close."""

    __tablename__ = "leads"

    # Primary key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Parcel reference (canonical key)
    apn: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Contact info from form or webhook
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Interest type (from LP form)
    interest_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Options: buying, selling, relocating, welcome_guide, exploring

    # Form message
    message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Web attribution
    page_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Which LP page
    referrer: Mapped[str | None] = mapped_column(String(500), nullable=True)   # HTTP referrer

    # Raw payload from webhook or form
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # LP internal ID (from webhook)
    lp_lead_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    # Pipeline stage
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="new", index=True)
    # Options: new, contacted, qualified, converted, closed

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    @property
    def full_name(self) -> str:
        """Return full name or empty string."""
        parts = [p for p in [self.first_name, self.last_name] if p]
        return " ".join(parts) or ""

    @property
    def is_active(self) -> bool:
        """Check if lead is still active."""
        return self.status not in ("closed", "converted")

    def advance(self, new_status: str) -> None:
        """Move lead to a new status. Validates status is known."""
        valid_statuses = ["new", "contacted", "qualified", "converted", "closed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Unknown status: {new_status}. Valid: {valid_statuses}")
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<Lead {self.id[:8]} APN={self.apn} status={self.status}>"
