from typing import Protocol

class FulfillmentService(Protocol):
    def mark_shipped(self, order_id, tracking_number: str | None = None) -> None: ...

class ManualFulfillmentStub:
    def mark_shipped(self, order_id, tracking_number=None):
        return None
