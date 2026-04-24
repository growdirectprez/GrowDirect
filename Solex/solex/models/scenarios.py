import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

SCENARIO_RUN_STATUSES = ("pending", "running", "succeeded", "failed", "partial")


class ScenarioRun(BaseModel):
    __tablename__ = "scenario_runs"
    scenario_name: Mapped[str] = mapped_column(String(80), nullable=False)
    params_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    summary_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    __table_args__ = (
        Index("ix_scenario_runs_name", "scenario_name"),
        Index("ix_scenario_runs_status", "status"),
    )
