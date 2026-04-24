import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel


class MagicLinkToken(BaseModel):
    __tablename__ = "magic_link_tokens"
    audience: Mapped[str] = mapped_column(String(16), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (Index("ix_mlt_audience_user", "audience", "user_id"),)
