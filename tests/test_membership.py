"""
Tests for membership module — Plan catalog and query functions.
"""

from src.membership import (
    get_plan,
    list_plans,
    get_plan_cost,
    get_plan_names,
)


class TestGetPlan:
    """Tests for the get_plan function."""

    def test_get_basic_plan(self):
        """Should return the Basic plan details."""
        plan = get_plan("basic")
        assert plan is not None
        assert plan["name"] == "Basic"
        assert plan["base_cost"] == 50

    def test_get_premium_plan(self):
        """Should return the Premium plan details."""
        plan = get_plan("premium")
        assert plan is not None
        assert plan["name"] == "Premium"
        assert plan["base_cost"] == 100

    def test_get_family_plan(self):
        """Should return the Family plan details."""
        plan = get_plan("family")
        assert plan is not None
        assert plan["name"] == "Family"
        assert plan["base_cost"] == 150

    def test_get_plan_case_insensitive_upper(self):
        """Should handle uppercase plan names via .lower() normalization."""
        plan = get_plan("BASIC")
        assert plan is not None
        assert plan["name"] == "Basic"

    def test_get_plan_case_insensitive_mixed(self):
        """Should handle mixed-case plan names via .lower() normalization."""
        plan = get_plan("Basic")
        assert plan is not None
        assert plan["name"] == "Basic"

    def test_get_nonexistent_plan(self):
        """Should return None for a non-existent plan."""
        plan = get_plan("platinum")
        assert plan is None

    def test_get_plan_with_none(self):
        """Should return None when None is passed."""
        plan = get_plan(None)
        assert plan is None

    def test_get_plan_with_number(self):
        """Should return None when a number is passed."""
        plan = get_plan(123)
        assert plan is None

    def test_get_plan_empty_string(self):
        """Should return None for an empty string."""
        plan = get_plan("")
        assert plan is None


class TestListPlans:
    """Tests for the list_plans function."""

    def test_returns_all_plans(self):
        """Should return all 3 plans."""
        plans = list_plans()
        assert len(plans) == 3

    def test_returns_list(self):
        """Should return a list."""
        plans = list_plans()
        assert isinstance(plans, list)

    def test_each_plan_has_required_fields(self):
        """Each plan should have name, base_cost, and benefits."""
        for plan in list_plans():
            assert "name" in plan
            assert "base_cost" in plan
            assert "benefits" in plan


class TestGetPlanCost:
    """Tests for the get_plan_cost function."""

    def test_basic_cost(self):
        """Basic plan should cost $50."""
        assert get_plan_cost("basic") == 50

    def test_premium_cost(self):
        """Premium plan should cost $100."""
        assert get_plan_cost("premium") == 100

    def test_family_cost(self):
        """Family plan should cost $150."""
        assert get_plan_cost("family") == 150

    def test_invalid_plan_returns_negative_one(self):
        """Non-existent plan should return -1."""
        assert get_plan_cost("platinum") == -1

    def test_none_returns_negative_one(self):
        """None input should return -1."""
        assert get_plan_cost(None) == -1


class TestGetPlanNames:
    """Tests for the get_plan_names function."""

    def test_returns_all_names(self):
        """Should return all plan keys."""
        names = get_plan_names()
        assert "basic" in names
        assert "premium" in names
        assert "family" in names

    def test_returns_list(self):
        """Should return a list."""
        assert isinstance(get_plan_names(), list)
