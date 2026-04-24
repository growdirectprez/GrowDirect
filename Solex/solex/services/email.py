"""EmailService — render + send templated emails via Flask-Mail, log all attempts."""
from __future__ import annotations

from datetime import datetime, timezone

from flask import current_app, render_template
from flask_mail import Message

from solex.extensions import db, mail
from solex.models import EmailLog

_SUBJECT_MAP = {
    "order_confirmation": "Your Solex order",
    "magic_link": "Your Solex sign-in link",
}


class EmailService:
    def send(self, template_name: str, to: str, **context) -> None:
        """Render and send an email, logging success or failure.

        Email delivery failures are captured in EmailLog.error — they do not
        propagate to the caller. Callers that need to react to failures should
        check the log or wrap this call themselves.
        """
        html = render_template(f"emails/{template_name}.html", **context)
        try:
            text = render_template(f"emails/{template_name}.txt", **context)
        except Exception:
            text = None

        msg = Message(
            subject=_SUBJECT_MAP.get(template_name, "Solex"),
            recipients=[to],
            body=text or "See HTML version.",
            html=html,
        )

        log = EmailLog(template=template_name, to=to)
        try:
            mail.send(msg)
            log.sent_at = datetime.now(timezone.utc)
        except Exception as exc:
            log.error = str(exc)[:500]
            current_app.logger.warning("email send failed: %s", exc)

        db.session.add(log)
        db.session.commit()
