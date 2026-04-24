from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel


class SquareWebhookEvent(BaseModel):
    __tablename__ = "square_webhook_events"
    square_event_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class EmailLog(BaseModel):
    __tablename__ = "email_logs"
    template: Mapped[str] = mapped_column(String(80), nullable=False)
    to: Mapped[str] = mapped_column(String(254), nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
