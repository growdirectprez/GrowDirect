import pytest
from solex.services.scenarios import registry
from solex.services.scenarios.base import Scenario


VALID_CATEGORIES = {
    "operations",
    "loss_prevention",
    "fraud",
    "customer_behavior",
    "subscriptions",
}


def _all_scenarios():
    registry._import_all()
    return registry.all_scenarios()


def test_all_nine_scenarios_declare_category():
    scenarios = _all_scenarios()
    assert len(scenarios) == 9
    for name, cls in scenarios.items():
        assert hasattr(cls, "category"), f"{name} missing category"
        assert cls.category in VALID_CATEGORIES, (
            f"{name}.category={cls.category!r} not in {VALID_CATEGORIES}"
        )


def test_all_nine_scenarios_declare_expected_behaviors():
    scenarios = _all_scenarios()
    for name, cls in scenarios.items():
        assert hasattr(cls, "expected_behaviors"), f"{name} missing expected_behaviors"
        eb = cls.expected_behaviors
        assert isinstance(eb, (list, tuple)), f"{name}.expected_behaviors must be list/tuple"
        assert len(eb) >= 1, f"{name}.expected_behaviors must have at least one entry"
        for entry in eb:
            assert isinstance(entry, str) and entry.strip(), (
                f"{name}.expected_behaviors entries must be non-empty strings"
            )


def test_registry_describe_returns_structured_dict():
    described = registry.describe("high_value_sale")
    assert isinstance(described, dict)
    assert described["name"] == "high_value_sale"
    assert described["category"] == "fraud"
    assert "description" in described and described["description"]
    assert "expected_behaviors" in described
    assert isinstance(described["expected_behaviors"], list)
    assert "expected_chirps" in described


def test_registry_describe_unknown_returns_none():
    assert registry.describe("does_not_exist") is None


def test_registry_by_category_groups_all_nine():
    grouped = registry.by_category()
    assert isinstance(grouped, dict)
    # Every key is a valid category
    for cat in grouped.keys():
        assert cat in VALID_CATEGORIES
    # Every scenario is placed exactly once
    total = sum(len(items) for items in grouped.values())
    assert total == 9
    flat_names = {item["name"] for items in grouped.values() for item in items}
    assert len(flat_names) == 9


def test_registry_by_category_canonical_placements():
    """Pin the category assignments so future scenario additions stay deliberate."""
    grouped = registry.by_category()
    name_to_category = {
        item["name"]: cat for cat, items in grouped.items() for item in items
    }
    expected = {
        "normal_retail_day": "operations",
        "after_hours_burst": "operations",
        "shrink_event": "loss_prevention",
        "high_value_sale": "fraud",
        "round_amount_cluster": "fraud",
        "refund_wave": "fraud",
        "cart_abandonment_cohort": "customer_behavior",
        "bulk_reseller_order": "customer_behavior",
        "autoship_cohort": "subscriptions",
    }
    assert name_to_category == expected
