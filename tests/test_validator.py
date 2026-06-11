"""
Tests for validator module — Input validation functions.
"""

from src.validator import (
    validate_plan,
    validate_features,
    validate_members,
    validate_confirmation,
)


class TestValidatePlan:
    """Tests for the validate_plan function."""

    def test_valid_basic(self):
        """'basic' should be valid."""
        is_valid, error = validate_plan("basic")
        assert is_valid is True
        assert error is None

    def test_valid_premium(self):
        """'premium' should be valid."""
        is_valid, error = validate_plan("premium")
        assert is_valid is True
        assert error is None

    def test_valid_family(self):
        """'family' should be valid."""
        is_valid, error = validate_plan("family")
        assert is_valid is True
        assert error is None

    def test_invalid_plan_name(self):
        """Non-existent plan should fail validation."""
        is_valid, error = validate_plan("platinum")
        assert is_valid is False
        assert "not available" in error

    def test_none_input(self):
        """None should fail with 'must be a string' error."""
        is_valid, error = validate_plan(None)
        assert is_valid is False
        assert "string" in error.lower()

    def test_empty_string(self):
        """Empty string should fail."""
        is_valid, error = validate_plan("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_whitespace_only(self):
        """Whitespace-only string should fail."""
        is_valid, error = validate_plan("   ")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_number_input(self):
        """Integer input should fail."""
        is_valid, error = validate_plan(123)
        assert is_valid is False
        assert "string" in error.lower()

    def test_list_input(self):
        """List input should fail."""
        is_valid, error = validate_plan(["basic"])
        assert is_valid is False
        assert "string" in error.lower()


class TestValidateFeatures:
    """Tests for the validate_features function."""

    def test_valid_single_feature(self):
        """Single valid feature should pass."""
        is_valid, error = validate_features(["personal_training"])
        assert is_valid is True
        assert error is None

    def test_valid_multiple_features(self):
        """Multiple valid features should pass."""
        is_valid, error = validate_features(
            ["personal_training", "group_classes"]
        )
        assert is_valid is True
        assert error is None

    def test_empty_list(self):
        """Empty feature list is valid (no features selected)."""
        is_valid, error = validate_features([])
        assert is_valid is True
        assert error is None

    def test_invalid_feature(self):
        """Non-existent feature should fail."""
        is_valid, error = validate_features(["swimming"])
        assert is_valid is False
        assert "not available" in error

    def test_not_a_list(self):
        """Non-list input should fail."""
        is_valid, error = validate_features("personal_training")
        assert is_valid is False
        assert "list" in error.lower()

    def test_none_input(self):
        """None should fail."""
        is_valid, error = validate_features(None)
        assert is_valid is False
        assert "list" in error.lower()

    def test_list_with_non_string(self):
        """List containing non-string should fail."""
        is_valid, error = validate_features([123])
        assert is_valid is False
        assert "string" in error.lower()

    def test_list_with_empty_string(self):
        """List containing empty string should fail."""
        is_valid, error = validate_features([""])
        assert is_valid is False
        assert "empty" in error.lower()

    def test_mixed_valid_and_invalid(self):
        """List with one valid and one invalid feature should fail."""
        is_valid, error = validate_features(["personal_training", "yoga"])
        assert is_valid is False
        assert "yoga" in error


class TestValidateMembers:
    """Tests for the validate_members function."""

    def test_valid_single_member(self):
        """1 member should be valid."""
        is_valid, error = validate_members(1)
        assert is_valid is True
        assert error is None

    def test_valid_multiple_members(self):
        """Multiple members should be valid."""
        is_valid, error = validate_members(5)
        assert is_valid is True
        assert error is None

    def test_zero_members(self):
        """0 members should be invalid."""
        is_valid, error = validate_members(0)
        assert is_valid is False
        assert "at least 1" in error

    def test_negative_members(self):
        """Negative members should be invalid."""
        is_valid, error = validate_members(-2)
        assert is_valid is False
        assert "at least 1" in error

    def test_string_input(self):
        """String input should be invalid."""
        is_valid, error = validate_members("two")
        assert is_valid is False
        assert "integer" in error.lower()

    def test_float_input(self):
        """Float input should be invalid."""
        is_valid, error = validate_members(2.5)
        assert is_valid is False
        assert "integer" in error.lower()

    def test_none_input(self):
        """None should be invalid."""
        is_valid, error = validate_members(None)
        assert is_valid is False
        assert "integer" in error.lower()


class TestValidateConfirmation:
    """Tests for the validate_confirmation function."""

    def test_true(self):
        """True should be valid."""
        is_valid, error = validate_confirmation(True)
        assert is_valid is True
        assert error is None

    def test_false(self):
        """False should be valid (user cancels, but input is valid)."""
        is_valid, error = validate_confirmation(False)
        assert is_valid is True
        assert error is None

    def test_string_input(self):
        """String input should be invalid."""
        is_valid, error = validate_confirmation("yes")
        assert is_valid is False
        assert "boolean" in error.lower()

    def test_integer_input(self):
        """Integer input should be invalid."""
        is_valid, error = validate_confirmation(1)
        assert is_valid is False
        assert "boolean" in error.lower()

    def test_none_input(self):
        """None should be invalid."""
        is_valid, error = validate_confirmation(None)
        assert is_valid is False
        assert "boolean" in error.lower()
