from typing import Protocol

class AddressValidator(Protocol):
    def validate(self, address: dict) -> tuple[bool, list[str]]: ...

class NoopValidator:
    REQUIRED = ("first_name", "last_name", "line1", "city", "region", "postal_code", "country")
    def validate(self, address: dict) -> tuple[bool, list[str]]:
        missing = [k for k in self.REQUIRED if not address.get(k)]
        return (not missing, missing)
