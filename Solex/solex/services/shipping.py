from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class ShippingQuote:
    shipping_cents: int
    label: str

class ShippingService(Protocol):
    def quote(self, subtotal_cents: int, region: str) -> ShippingQuote: ...

class FlatRateShippingStub:
    def __init__(self, flat_cents: int, free_threshold_cents: int):
        self.flat_cents = flat_cents
        self.free_threshold_cents = free_threshold_cents
    def quote(self, subtotal_cents: int, region: str) -> ShippingQuote:
        if subtotal_cents >= self.free_threshold_cents:
            return ShippingQuote(shipping_cents=0, label="Free ground")
        return ShippingQuote(shipping_cents=self.flat_cents, label="Flat ground")
