from typing import Type

_registry: dict[str, Type] = {}


def register(cls):
    """Class decorator to register a Scenario subclass."""
    name = getattr(cls, "name", None)
    if not name:
        raise ValueError(f"{cls.__name__} has no `name` class attribute")
    if name in _registry:
        raise ValueError(f"scenario name collision: {name}")
    _registry[name] = cls
    return cls


def get(name: str):
    return _registry.get(name)


def all_scenarios():
    return dict(_registry)


def _import_all():
    """Force-import each scenario module so decorators fire."""
    # Import all scenario modules here once they exist. For Chunk 1,
    # none of the 9 scenario modules have been created yet — that's fine,
    # the registry is still testable with manually registered classes.
    try:
        from solex.services.scenarios import (  # noqa: F401
            normal_retail_day, after_hours_burst, round_amount_cluster,
            high_value_sale, autoship_cohort, bulk_reseller_order,
            refund_wave, shrink_event, cart_abandonment_cohort,
        )
    except ImportError:
        # Scenarios not yet implemented — acceptable during chunk-by-chunk dev
        pass
