import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
from sqlalchemy.orm import Session

from solex.models import AdminUser, Customer, MagicLinkToken

MAGIC_LINK_TTL = timedelta(minutes=20)


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def verify_admin_password(self, email: str, password: str) -> Optional[AdminUser]:
        user = self.session.execute(
            select(AdminUser).where(AdminUser.email == email, AdminUser.active == True)
        ).scalar_one_or_none()
        if user is None or not user.password_hash:
            return None
        return user if check_password_hash(user.password_hash, password) else None

    def set_admin_password(self, user: AdminUser, password: str):
        user.password_hash = generate_password_hash(password)
        self.session.flush()

    def issue_magic_link(self, audience: str, user_id) -> str:
        assert audience in ("admin", "customer")
        token = secrets.token_urlsafe(32)
        self.session.add(MagicLinkToken(
            audience=audience,
            user_id=user_id,
            token_hash=_hash(token),
            expires_at=datetime.now(timezone.utc) + MAGIC_LINK_TTL,
        ))
        self.session.flush()
        return token

    def consume_magic_link(self, audience: str, token: str):
        row = self.session.execute(
            select(MagicLinkToken).where(
                MagicLinkToken.audience == audience,
                MagicLinkToken.token_hash == _hash(token),
            )
        ).scalar_one_or_none()
        if row is None or row.consumed_at is not None:
            return None
        if row.expires_at < datetime.now(timezone.utc):
            return None
        row.consumed_at = datetime.now(timezone.utc)
        self.session.flush()
        Model = AdminUser if audience == "admin" else Customer
        return self.session.get(Model, row.user_id)
