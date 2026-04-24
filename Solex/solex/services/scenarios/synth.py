"""Fake-data generators for scenario cohorts. Deterministic given a seed."""
import random
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass


@dataclass(frozen=True)
class SynthCustomer:
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class SynthAddress:
    line1: str
    city: str
    region: str
    postal_code: str


_FIRST_NAMES = ("Maya", "Chen", "Priya", "Alex", "Sam", "Jordan", "Taylor",
                "Riley", "Casey", "Morgan", "Avery", "Emerson", "Sage", "Rowan")
_LAST_NAMES = ("Park", "Rivera", "Kim", "Patel", "Nguyen", "Singh", "Hernandez",
               "Ochoa", "Brooks", "Wells", "Vogel", "Tran", "Cole", "Hart")
_CITIES = (("Torrance", "CA", "90503"), ("Redondo Beach", "CA", "90277"),
           ("Palos Verdes Estates", "CA", "90274"), ("San Pedro", "CA", "90731"),
           ("Rolling Hills", "CA", "90274"), ("Manhattan Beach", "CA", "90266"),
           ("Long Beach", "CA", "90802"), ("Carson", "CA", "90745"))


def synth_customer(rng: random.Random, run_tag: str, i: int) -> SynthCustomer:
    first = rng.choice(_FIRST_NAMES)
    last = rng.choice(_LAST_NAMES)
    email = f"{first.lower()}.{last.lower()}.{run_tag}.{i}@solex.local"
    return SynthCustomer(first_name=first, last_name=last, email=email)


def synth_address(rng: random.Random) -> SynthAddress:
    num = rng.randint(100, 9999)
    street = rng.choice(("Main St", "Ocean Ave", "Palos Verdes Dr", "Crest Rd",
                         "Hawthorne Blvd", "Torrance Blvd", "Anza Ave"))
    city, region, zip5 = rng.choice(_CITIES)
    return SynthAddress(line1=f"{num} {street}", city=city, region=region, postal_code=zip5)


def pick_time_in_window(rng: random.Random, start_hour: int, end_hour: int,
                        *, base: datetime | None = None) -> datetime:
    """Pick a datetime in today's [start_hour, end_hour) window. end_hour may wrap past midnight
    (e.g., start=22, end=2 means 22:00 of base through 02:00 of base + 1 day)."""
    base = (base or datetime.now(timezone.utc)).replace(
        hour=0, minute=0, second=0, microsecond=0)
    if end_hour <= start_hour:
        total_minutes = (24 - start_hour + end_hour) * 60
    else:
        total_minutes = (end_hour - start_hour) * 60
    offset = rng.randint(0, total_minutes - 1)
    return base + timedelta(hours=start_hour, minutes=offset)
