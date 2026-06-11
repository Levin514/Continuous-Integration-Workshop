"""
Validator module — Input validation for gym membership system.

Provides functions to validate user inputs such as plan names,
feature selections, and member counts before processing.
"""

from src.membership import get_plan
from src.features import get_feature


def validate_plan(plan_name):
    """
    Validate that a plan name is a non-empty string and exists in the catalog.

    Args:
        plan_name: The plan name to validate.

    Returns:
        tuple: (is_valid, error_message)
            - (True, None) if valid.
            - (False, str) if invalid, with a descriptive error.
    """
    if not isinstance(plan_name, str):
        return False, "Plan name must be a string."

    if not plan_name.strip():
        return False, "Plan name cannot be empty."

    if get_plan(plan_name) is None:
        return False, f"Plan '{plan_name}' is not available. Valid plans: basic, premium, family."

    return True, None


def validate_features(feature_names):
    """
    Validate that feature_names is a list of valid feature keys.

    Args:
        feature_names: The list of feature names to validate.

    Returns:
        tuple: (is_valid, error_message)
            - (True, None) if all features are valid.
            - (False, str) if any feature is invalid.
    """
    if not isinstance(feature_names, list):
        return False, "Features must be provided as a list."

    for name in feature_names:
        if not isinstance(name, str):
            return False, f"Each feature name must be a string, got {type(name).__name__}."

        if not name.strip():
            return False, "Feature name cannot be empty."

        if get_feature(name) is None:
            return (
                False,
                f"Feature '{name}' is not available. "
                f"Valid features: personal_training, group_classes, exclusive_facilities.",
            )

    return True, None


def validate_members(members):
    """
    Validate the number of members for group discount calculation.

    Args:
        members: The number of members to validate.

    Returns:
        tuple: (is_valid, error_message)
            - (True, None) if valid (positive integer).
            - (False, str) if invalid.
    """
    if not isinstance(members, int):
        return False, "Number of members must be an integer."

    if members < 1:
        return False, "Number of members must be at least 1."

    return True, None


def validate_confirmation(confirmed):
    """
    Validate the confirmation input.

    Args:
        confirmed: Boolean indicating user confirmation.

    Returns:
        tuple: (is_valid, error_message)
            - (True, None) if confirmed is a boolean.
            - (False, str) if not a boolean.
    """
    if not isinstance(confirmed, bool):
        return False, "Confirmation must be a boolean value (true/false)."

    return True, None
