from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class TaxCalculation:
    tax_cents: int

class TaxService(Protocol):
    def compute(self, subtotal_cents: int, shipping_cents: int, region: str) -> TaxCalculation: ...

class FlatRateTaxStub:
    def __init__(self, rate_pct: float):
        self.rate_pct = rate_pct
    def compute(self, subtotal_cents: int, shipping_cents: int, region: str) -> TaxCalculation:
        total = subtotal_cents + shipping_cents
        return TaxCalculation(tax_cents=round(total * (self.rate_pct / 100.0)))
