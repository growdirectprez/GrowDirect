import uuid
from typing import Optional
from flask_login import UserMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel


class Customer(UserMixin, BaseModel):
    __tablename__ = "customers"
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    square_customer_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    # default_address_id intentionally omitted in Plan 1 — would create a circular FK
    # (customers.default_address_id → addresses.id, addresses.customer_id → customers.id)
    # that Alembic autogen doesn't order correctly without use_alter. Plan 2 adds it
    # back with the full account surface.
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan",
    )


class Address(BaseModel):
    __tablename__ = "addresses"
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False,
    )
    label: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    line1: Mapped[str] = mapped_column(String(200), nullable=False)
    line2: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    region: Mapped[str] = mapped_column(String(80), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(2), default="US", nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    customer: Mapped["Customer"] = relationship(back_populates="addresses")
