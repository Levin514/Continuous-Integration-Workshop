"""
Gym Membership Management System — FastAPI Application.

Provides REST API endpoints for managing gym memberships,
calculating costs with discounts, and validating inputs.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from src.membership import list_plans, get_plan
from src.features import list_features, get_feature
from src.calculator import calculate_total, get_membership_summary

app = FastAPI(
    title="Gym Membership Management System",
    description="API for managing gym membership plans, features, and cost calculations.",
    version="1.0.0",
)


class MembershipRequest(BaseModel):
    """Request body for membership calculation."""

    plan: str
    features: list[str] = []
    members: int = 1
    confirmed: bool = True


class MembershipResponse(BaseModel):
    """Response body for membership calculation."""

    total: int
    summary: dict | None = None
    error: str | None = None


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "gym-membership-api"}


# ──────────────────────────────────────────────
# Plans
# ──────────────────────────────────────────────

@app.get("/plans", tags=["Plans"])
def get_all_plans():
    """List all available membership plans."""
    return {"plans": list_plans()}


@app.get("/plans/{plan_name}", tags=["Plans"])
def get_plan_details(plan_name: str):
    """Get details of a specific membership plan."""
    plan = get_plan(plan_name)
    if plan is None:
        return {
            "error": f"Plan '{plan_name}' not found.",
            "available_plans": ["basic", "premium", "family"],
        }
    return {"plan": plan}


# ──────────────────────────────────────────────
# Features
# ──────────────────────────────────────────────

@app.get("/features", tags=["Features"])
def get_all_features():
    """List all available additional features."""
    return {"features": list_features()}


@app.get("/features/{feature_name}", tags=["Features"])
def get_feature_details(feature_name: str):
    """Get details of a specific feature."""
    feature = get_feature(feature_name)
    if feature is None:
        return {
            "error": f"Feature '{feature_name}' not found.",
            "available_features": [
                "personal_training",
                "group_classes",
                "exclusive_facilities",
            ],
        }
    return {"feature": feature}


# ──────────────────────────────────────────────
# Calculator
# ──────────────────────────────────────────────

@app.post("/calculate", tags=["Calculator"], response_model=MembershipResponse)
def calculate_membership(request: MembershipRequest):
    """
    Calculate total membership cost with all applicable discounts/surcharges.

    Order of operations:
    1. Base cost + feature costs
    2. Group discount (10% for 2+ members)
    3. Premium surcharge (15% if premium features selected)
    4. Amount discount ($20 for >$200, $50 for >$400)
    """
    total, summary, error = calculate_total(
        request.plan,
        request.features,
        request.members,
        request.confirmed,
    )
    return MembershipResponse(total=total, summary=summary, error=error)


@app.post("/preview", tags=["Calculator"])
def preview_membership(request: MembershipRequest):
    """
    Preview membership cost summary without confirming.

    Returns the same breakdown as /calculate but is intended
    for the 'review before confirm' step.
    """
    summary, error = get_membership_summary(
        request.plan,
        request.features,
        request.members,
    )
    if error:
        return {"error": error, "summary": None}
    return {"summary": summary, "error": None}
