"""
Tests for calculator module — Cost calculation, discounts, and surcharges.
"""

import pytest

from src.calculator import (
    calculate_base_total,
    apply_group_discount,
    apply_premium_surcharge,
    apply_amount_discount,
    calculate_total,
    get_membership_summary,
)


class TestCalculateBaseTotal:
    """Tests for the calculate_base_total function."""

    def test_basic_no_features(self):
        """Basic plan with no features should return base cost only."""
        total, error = calculate_base_total("basic", [])
        assert total == 50
        assert error is None

    def test_premium_with_group_classes(self):
        """Premium plan with group classes."""
        total, error = calculate_base_total("premium", ["group_classes"])
        assert total == 120
        assert error is None

    def test_family_with_all_features(self):
        """Family plan with all features."""
        total, error = calculate_base_total(
            "family",
            ["personal_training", "group_classes", "exclusive_facilities"],
        )
        assert total == 225  # 150 + 30 + 20 + 25
        assert error is None

    def test_invalid_plan_returns_error(self):
        """Invalid plan should return -1 with error message."""
        total, error = calculate_base_total("gold", [])
        assert total == -1
        assert error is not None
        assert "gold" in error

    def test_invalid_feature_returns_error(self):
        """Invalid feature should return -1 with error message."""
        total, error = calculate_base_total("basic", ["swimming"])
        assert total == -1
        assert error is not None
        assert "swimming" in error


class TestApplyGroupDiscount:
    """Tests for the apply_group_discount function."""

    def test_single_member_no_discount(self):
        """1 member should get no discount."""
        assert apply_group_discount(100, 1) == 100

    def test_two_members_ten_percent_off(self):
        """2 members should get 10% off."""
        assert apply_group_discount(100, 2) == 90.0

    def test_five_members_ten_percent_off(self):
        """5 members should also get 10% off (same rate)."""
        assert apply_group_discount(200, 5) == 180.0

    def test_zero_members_no_discount(self):
        """0 members (edge case) should get no discount."""
        assert apply_group_discount(100, 0) == 100


class TestApplyPremiumSurcharge:
    """Tests for the apply_premium_surcharge function."""

    def test_no_premium_features(self):
        """No premium features → no surcharge."""
        assert apply_premium_surcharge(100, ["group_classes"]) == 100

    def test_with_personal_training(self):
        """Personal training is premium → 15% surcharge."""
        result = apply_premium_surcharge(100, ["personal_training"])
        assert result == pytest.approx(115.0)

    def test_with_exclusive_facilities(self):
        """Exclusive facilities is premium → 15% surcharge."""
        result = apply_premium_surcharge(200, ["exclusive_facilities"])
        assert result == pytest.approx(230.0)

    def test_empty_features(self):
        """No features at all → no surcharge."""
        assert apply_premium_surcharge(100, []) == 100

    def test_mixed_features(self):
        """Mix of premium and non-premium → surcharge applied."""
        result = apply_premium_surcharge(100, ["group_classes", "personal_training"])
        assert result == pytest.approx(115.0)


class TestApplyAmountDiscount:
    """Tests for the apply_amount_discount function."""

    def test_under_200_no_discount(self):
        """Total <= $200 → no discount."""
        assert apply_amount_discount(200) == 200
        assert apply_amount_discount(150) == 150

    def test_over_200_under_400(self):
        """Total > $200 and <= $400 → $20 discount."""
        assert apply_amount_discount(201) == 181
        assert apply_amount_discount(300) == 280
        assert apply_amount_discount(400) == 380

    def test_over_400(self):
        """Total > $400 → $50 discount."""
        assert apply_amount_discount(401) == 351
        assert apply_amount_discount(500) == 450

    def test_exact_200(self):
        """Exactly $200 → no discount (not > $200)."""
        assert apply_amount_discount(200) == 200

    def test_exact_400(self):
        """Exactly $400 → $20 discount (> $200 but not > $400)."""
        assert apply_amount_discount(400) == 380


class TestCalculateTotal:
    """Tests for the main calculate_total function."""

    def test_basic_no_features_single_member(self):
        """Simple case: basic plan, no features, 1 member."""
        total, summary, error = calculate_total("basic", [], 1, True)
        assert total == 50
        assert error is None
        assert summary["plan"] == "basic"

    def test_premium_with_personal_training(self):
        """Premium + personal training → surcharge applied."""
        # base: 100 + 30 = 130
        # no group discount (1 member)
        # premium surcharge: 130 * 1.15 = 149.5 → 150
        # no amount discount (< 200)
        total, _, error = calculate_total(
            "premium", ["personal_training"], 1, True
        )
        assert error is None
        assert total == 150  # round(149.5) = 150

    def test_family_all_features_group(self):
        """Family + all features + 3 members → group + premium + amount discounts."""
        # base: 150 + 30 + 20 + 25 = 225
        # group discount (3 members): 225 * 0.9 = 202.5
        # premium surcharge (personal_training is premium): 202.5 * 1.15 = 232.875
        # amount discount (> 200): 232.875 - 20 = 212.875 → 213
        total, summary, error = calculate_total(
            "family",
            ["personal_training", "group_classes", "exclusive_facilities"],
            3,
            True,
        )
        assert error is None
        assert total == 213
        assert summary["group_discount_applied"] is True
        assert summary["premium_surcharge_applied"] is True

    def test_cancelled_returns_negative_one(self):
        """Cancelled membership should return -1."""
        total, summary, error = calculate_total("basic", [], 1, False)
        assert total == -1
        assert summary is None
        assert "cancelled" in error.lower()

    def test_invalid_plan_returns_negative_one(self):
        """Invalid plan should return -1."""
        total, _, error = calculate_total("gold", [], 1, True)
        assert total == -1
        assert error is not None

    def test_invalid_feature_returns_negative_one(self):
        """Invalid feature should return -1."""
        total, _, error = calculate_total("basic", ["swimming"], 1, True)
        assert total == -1
        assert error is not None

    def test_invalid_members_returns_negative_one(self):
        """Invalid members count should return -1."""
        total, _, error = calculate_total("basic", [], -1, True)
        assert total == -1
        assert error is not None

    def test_zero_members_returns_negative_one(self):
        """Zero members should return -1."""
        total, _, error = calculate_total("basic", [], 0, True)
        assert total == -1
        assert "at least 1" in error.lower()

    def test_non_boolean_confirmation(self):
        """Non-boolean confirmation should return -1."""
        total, _, error = calculate_total("basic", [], 1, "yes")
        assert total == -1
        assert "boolean" in error.lower()

    def test_group_discount_two_members(self):
        """Two members should trigger group discount."""
        # basic: 50, no features
        # group: 50 * 0.9 = 45
        # no surcharge, no amount discount
        total, summary, error = calculate_total("basic", [], 2, True)
        assert error is None
        assert total == 45
        assert summary["group_discount_applied"] is True

    def test_amount_discount_over_200(self):
        """Total > $200 after surcharges → $20 discount."""
        # family: 150, personal_training: 30, exclusive: 25 → base: 205
        # no group (1 member)
        # premium surcharge: 205 * 1.15 = 235.75
        # amount discount (> $200): 235.75 - 20 = 215.75 → 216
        total, _, error = calculate_total(
            "family", ["personal_training", "exclusive_facilities"], 1, True
        )
        assert error is None
        assert total == 216


class TestGetMembershipSummary:
    """Tests for the get_membership_summary function."""

    def test_valid_summary(self):
        """Should return a valid summary dict."""
        summary, error = get_membership_summary("basic", [], 1)
        assert error is None
        assert summary is not None
        assert "plan" in summary
        assert "final_total" in summary

    def test_invalid_plan_summary(self):
        """Invalid plan should return error."""
        summary, error = get_membership_summary("gold", [], 1)
        assert summary is None
        assert error is not None
