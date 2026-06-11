"""
Features module — Manages additional gym features.

Provides the catalog of optional features that members can add
to their membership. Each feature has a name, cost, and a flag
indicating whether it is a premium feature (triggers surcharge).
"""

# Feature catalog: each feature has name, cost, and is_premium flag
FEATURES = {
    "personal_training": {
        "name": "Personal Training",
        "cost": 30,
        "is_premium": True,
    },
    "group_classes": {
        "name": "Group Classes",
        "cost": 20,
        "is_premium": False,
    },
    "exclusive_facilities": {
        "name": "Exclusive Facilities",
        "cost": 25,
        "is_premium": True,
    },
}


def get_feature(feature_name):
    """
    Retrieve a feature by its name (case-insensitive).

    Args:
        feature_name: Name/key of the feature to look up.

    Returns:
        dict: Feature details (name, cost, is_premium) if found.
        None: If the feature does not exist.
    """
    if not isinstance(feature_name, str):
        return None
    return FEATURES.get(feature_name.lower())


def list_features():
    """
    List all available additional features.

    Returns:
        list[dict]: A list of all feature dictionaries.
    """
    return list(FEATURES.values())


def get_feature_cost(feature_name):
    """
    Get the cost for a given feature.

    Args:
        feature_name: Name/key of the feature.

    Returns:
        int: Cost of the feature if found.
        -1: If the feature does not exist.
    """
    feature = get_feature(feature_name)
    if feature is None:
        return -1
    return feature["cost"]


def get_feature_names():
    """
    Get a list of all valid feature name keys.

    Returns:
        list[str]: List of feature keys (lowercase).
    """
    return list(FEATURES.keys())


def has_premium_features(feature_names):
    """
    Check if any of the given features are premium.

    Args:
        feature_names: List of feature name keys to check.

    Returns:
        bool: True if at least one feature is premium, False otherwise.
    """
    for name in feature_names:
        feature = get_feature(name)
        if feature and feature["is_premium"]:
            return True
    return False


def calculate_features_cost(feature_names):
    """
    Calculate the total cost of a list of features.

    Args:
        feature_names: List of feature name keys.

    Returns:
        tuple: (total_cost, error_message)
            - (int, None) if all features are valid.
            - (-1, str) if any feature is invalid.
    """
    total = 0
    for name in feature_names:
        cost = get_feature_cost(name)
        if cost == -1:
            return -1, f"Feature '{name}' is not available."
        total += cost
    return total, None
