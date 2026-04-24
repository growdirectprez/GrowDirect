# solex/services/returns.py
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from solex.models import ReturnRequest, Order, AdminUser
from solex.services.refunds import RefundsService
from solex.services.email import EmailService

class ReturnsError(Exception): ...

class ReturnsService:
    def __init__(self, session: Session, refunds: RefundsService,
                 email: Optional[EmailService] = None):
        self.session = session
        self.refunds = refunds
        self.email = email or EmailService()

    def request(self, order: Order, reason: str) -> ReturnRequest:
        req = ReturnRequest(
            order_id=order.id, customer_id=order.customer_id,
            reason=reason, status="pending",
        )
        self.session.add(req); self.session.commit()
        return req

    def approve(self, req: ReturnRequest, admin: AdminUser) -> ReturnRequest:
        if req.status != "pending":
            raise ReturnsError(f"cannot approve from status={req.status}")
        order = self.session.get(Order, req.order_id)
        refund = self.refunds.issue_refund(order, order.total_cents,
                                           reason=f"return:{req.id}")
        req.refund_id = refund.id
        req.status = "completed"
        req.approved_by_admin_user_id = admin.id
        req.resolved_at = datetime.now(timezone.utc)
        self.session.commit()
        try:
            self.email.send("return_approved", to=order.customer_email,
                            order=order, return_request=req)
        except Exception:
            pass
        return req

    def deny(self, req: ReturnRequest, admin: AdminUser, reason: str = "") -> ReturnRequest:
        if req.status != "pending":
            raise ReturnsError(f"cannot deny from status={req.status}")
        req.status = "denied"
        req.approved_by_admin_user_id = admin.id
        req.resolved_at = datetime.now(timezone.utc)
        self.session.commit()
        return req
