# solex/services/abandonment.py
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from solex.models import Cart
from solex.services.email import EmailService

# Delay before the first nudge email is sent
FIRST_NUDGE_DELAY = timedelta(hours=1)


class AbandonmentService:
    def __init__(self, session: Session, email: EmailService):
        self.session = session
        self.email = email

    def sweep(self) -> dict:
        """Scan carts for abandonment candidates and send nudge emails.

        Sends a first nudge to any cart that:
          - has at least one line
          - has a known customer (so we have an email address)
          - has not been recovered
          - has not already received an abandonment email
          - has been inactive for at least FIRST_NUDGE_DELAY

        Returns a summary dict with counts.
        """
        summary = {"first_nudge": 0}
        cutoff = datetime.now(timezone.utc) - FIRST_NUDGE_DELAY

        carts = self.session.execute(
            select(Cart)
            .options(joinedload(Cart.customer), joinedload(Cart.lines))
            .where(
                Cart.last_activity_at <= cutoff,
                Cart.abandonment_emailed_at.is_(None),
                Cart.recovered_at.is_(None),
                Cart.customer_id.is_not(None),
            )
        ).unique().scalars().all()

        for cart in carts:
            if not cart.lines:
                continue
            if cart.customer is None or not cart.customer.email:
                continue
            try:
                self.email.send(
                    "cart_abandonment",
                    to=cart.customer.email,
                    cart=cart,
                )
                cart.abandonment_emailed_at = datetime.now(timezone.utc)
                self.session.commit()
                summary["first_nudge"] += 1
            except Exception:
                self.session.rollback()

        return summary
