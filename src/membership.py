"""
Membership module — Manages gym membership plans.

Provides the catalog of available plans and functions to query them.
Each plan has a name, base cost, and a list of included benefits.
"""

# Plan catalog: each plan is a dict with name, base_cost, and benefits
PLANS = {
    "basic": {
        "name": "Basic",
        "base_cost": 50,
        "benefits": [
            "Access to gym floor",
            "Locker room access",
        ],
    },
    "premium": {
        "name": "Premium",
        "base_cost": 100,
        "benefits": [
            "Access to gym floor",
            "Locker room access",
            "Pool access",
            "Sauna access",
            "Priority booking",
        ],
    },
    "family": {
        "name": "Family",
        "base_cost": 150,
        "benefits": [
            "Access to gym floor",
            "Locker room access",
            "Pool access",
            "Sauna access",
            "Priority booking",
            "Up to 4 family members",
        ],
    },
}


def get_plan(plan_name):
    """
    Retrieve a membership plan by its name (case-insensitive).

    Args:
        plan_name: Name of the plan to look up.

    Returns:
        dict: Plan details (name, base_cost, benefits) if found.
        None: If the plan does not exist.
    """
    if not isinstance(plan_name, str):
        return None
    return PLANS.get(plan_name.lower())


def list_plans():
    """
    List all available membership plans.

    Returns:
        list[dict]: A list of all plan dictionaries.
    """
    return list(PLANS.values())


def get_plan_cost(plan_name):
    """
    Get the base cost for a given plan.

    Args:
        plan_name: Name of the plan.

    Returns:
        int: Base cost of the plan if found.
        -1: If the plan does not exist.
    """
    plan = get_plan(plan_name)
    if plan is None:
        return -1
    return plan["base_cost"]


def get_plan_names():
    """
    Get a list of all valid plan names.

    Returns:
        list[str]: List of plan name keys (lowercase).
    """
    return list(PLANS.keys())
