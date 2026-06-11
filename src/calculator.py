"""
Calculator module — Cost calculation and discount logic.

Implements the complete pricing engine for gym memberships:
1. Base cost from plan selection
2. Additional features cost
3. Group discount (10% for 2+ members on same plan)
4. Premium surcharge (15% if any premium feature selected)
5. Amount-based discounts ($20 for >$200, $50 for >$400)

Order of operations:
  base + features → group discount → premium surcharge → amount discount
"""

from src.membership import get_plan_cost
from src.features import calculate_features_cost, has_premium_features
from src.validator import (
    validate_plan,
    validate_features,
    validate_members,
    validate_confirmation,
)

# Discount and surcharge constants
GROUP_DISCOUNT_THRESHOLD = 2
GROUP_DISCOUNT_RATE = 0.10
PREMIUM_SURCHARGE_RATE = 0.15
AMOUNT_DISCOUNT_TIER_1_THRESHOLD = 200
AMOUNT_DISCOUNT_TIER_1_VALUE = 20
AMOUNT_DISCOUNT_TIER_2_THRESHOLD = 400
AMOUNT_DISCOUNT_TIER_2_VALUE = 50


def calculate_base_total(plan_name, feature_names):
    """
    Calculate the raw total before any discounts or surcharges.

    Args:
        plan_name: The selected membership plan key.
        feature_names: List of selected feature keys.

    Returns:
        tuple: (base_total, error_message)
            - (float, None) on success.
            - (-1, str) on validation error.
    """
    is_valid, error = validate_plan(plan_name)
    if not is_valid:
        return -1, error

    is_valid, error = validate_features(feature_names)
    if not is_valid:
        return -1, error

    plan_cost = get_plan_cost(plan_name)
    features_cost, error = calculate_features_cost(feature_names)

    if features_cost == -1:
        return -1, error

    return plan_cost + features_cost, None


def apply_group_discount(total, members):
    """
    Apply group discount if 2 or more members choose the same plan.

    10% discount on the total for groups of 2+.

    Args:
        total: Current total amount.
        members: Number of members on the same plan.

    Returns:
        float: Discounted total (unchanged if members < 2).
    """
    if members >= GROUP_DISCOUNT_THRESHOLD:
        return total * (1 - GROUP_DISCOUNT_RATE)
    return total


def apply_premium_surcharge(total, feature_names):
    """
    Apply 15% premium surcharge if any selected feature is premium.

    Args:
        total: Current total amount.
        feature_names: List of selected feature keys.

    Returns:
        float: Total with surcharge applied (unchanged if no premium features).
    """
    if has_premium_features(feature_names):
        return total * (1 + PREMIUM_SURCHARGE_RATE)
    return total


def apply_amount_discount(total):
    """
    Apply amount-based discount tiers.

    - If total > $400 → subtract $50
    - Elif total > $200 → subtract $20

    Args:
        total: Current total amount.

    Returns:
        float: Total after amount discount.
    """
    if total > AMOUNT_DISCOUNT_TIER_2_THRESHOLD:
        return total - AMOUNT_DISCOUNT_TIER_2_VALUE
    if total > AMOUNT_DISCOUNT_TIER_1_THRESHOLD:
        return total - AMOUNT_DISCOUNT_TIER_1_VALUE
    return total


def calculate_total(plan_name, feature_names, members=1, confirmed=True):
    """
    Calculate the final membership cost with all discounts and surcharges.

    Order of operations:
        1. base_cost + features_cost
        2. Group discount (if members >= 2)
        3. Premium surcharge (if any premium feature)
        4. Amount discount (tier-based)

    Args:
        plan_name: The selected membership plan key.
        feature_names: List of selected feature keys.
        members: Number of members on the same plan (default: 1).
        confirmed: Whether the user confirmed the purchase (default: True).

    Returns:
        tuple: (total, summary, error_message)
            - (int, dict, None) on success (total is a positive integer).
            - (-1, None, str) on error or cancellation.
    """
    # Validate members
    is_valid, error = validate_members(members)
    if not is_valid:
        return -1, None, error

    # Validate confirmation
    is_valid, error = validate_confirmation(confirmed)
    if not is_valid:
        return -1, None, error

    # Check if user cancelled
    if not confirmed:
        return -1, None, "Membership registration cancelled by user."

    # Calculate base total
    base_total, error = calculate_base_total(plan_name, feature_names)
    if base_total == -1:
        return -1, None, error

    # Apply discounts and surcharges in order
    total = float(base_total)
    after_group = apply_group_discount(total, members)
    after_premium = apply_premium_surcharge(after_group, feature_names)
    final_total = apply_amount_discount(after_premium)

    # Build summary
    summary = {
        "plan": plan_name,
        "features": feature_names,
        "members": members,
        "base_total": base_total,
        "after_group_discount": round(after_group, 2),
        "after_premium_surcharge": round(after_premium, 2),
        "final_total": int(round(final_total)),
        "group_discount_applied": members >= GROUP_DISCOUNT_THRESHOLD,
        "premium_surcharge_applied": has_premium_features(feature_names),
        "amount_discount_applied": (
            AMOUNT_DISCOUNT_TIER_2_VALUE if final_total != after_premium
            else (
                AMOUNT_DISCOUNT_TIER_1_VALUE
                if after_premium > AMOUNT_DISCOUNT_TIER_1_THRESHOLD
                and final_total != after_premium
                else 0
            )
        ),
    }

    final_int = int(round(final_total))

    # Ensure positive result
    if final_int < 0:
        return -1, None, "Calculated total is negative. Please check inputs."

    return final_int, summary, None


def get_membership_summary(plan_name, feature_names, members=1):
    """
    Generate a human-readable summary of the membership selection.

    This is the 'preview before confirmation' — does NOT finalize.

    Args:
        plan_name: The selected membership plan key.
        feature_names: List of selected feature keys.
        members: Number of members on the same plan.

    Returns:
        tuple: (summary_dict, error_message)
            - (dict, None) on success.
            - (None, str) on validation error.
    """
    total, summary, error = calculate_total(
        plan_name, feature_names, members, confirmed=True
    )
    if total == -1:
        return None, error
    return summary, None
