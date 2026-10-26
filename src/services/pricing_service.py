"""Advisory demonstration pricing helpers.

Recommendations never change a stored price. A transparent heuristic is used
so the pricing page can show a complete recommendation, comparison table and
chart. Replace generate_recommendation() later with a validated regression model.
"""

from __future__ import annotations

from copy import deepcopy

from src.services.demo_data import store

MODEL_STATUS = (
    "Pricing model not connected. The values below are a labelled "
    "demonstration response for interface development."
)


def list_products() -> list[dict]:
    return [_with_gaps(item) for item in store.products]


def get_product(product_id: str) -> dict | None:
    for item in store.products:
        if item["id"] == product_id:
            return _with_gaps(item)
    return None


def comparison_table() -> list[dict]:
    return list_products()


def generate_recommendation(product_id: str) -> dict:
    product = get_product(product_id)
    if product is None:
        return {
            "connected": False,
            "error": "Select a product first.",
        }

    current = product["current_price"]
    cost = product["cost"]
    competitor = product["competitor_price"]
    floor = round(cost * 1.10, 2)
    difference = round(current - competitor, 2)
    percent = round((difference / competitor) * 100, 1) if competitor else 0.0

    if current > competitor:
        proposed = round(current - abs(difference) * 0.4, 2)
        direction = "decrease"
    elif current < competitor:
        proposed = round(current + abs(difference) * 0.4, 2)
        direction = "increase"
    else:
        proposed = current
        direction = "hold"

    if proposed < floor:
        proposed = floor
        direction = "hold-at-floor"

    adjustment = round(proposed - current, 2)
    explanation = (
        "Demonstration heuristic only — not a trained pricing model. "
        "The prototype moves 40% of the gap toward the listed competitor price, "
        f"then keeps the proposal at or above a 10% mark-up on cost (P{floor:,.2f}). "
        "This is advisory and does not change any selling price."
    )

    return {
        "connected": False,
        "model_status": MODEL_STATUS,
        "product": product,
        "current_price": current,
        "cost": cost,
        "competitor_price": competitor,
        "price_difference": difference,
        "percent_difference": percent,
        "suggested_adjustment": adjustment,
        "proposed_price": proposed,
        "direction": direction,
        "floor_price": floor,
        "explanation": explanation,
    }


def chart_payload(recommendation: dict | None = None) -> dict:
    products = list_products()
    labels = [item["name"] for item in products]
    current = [item["current_price"] for item in products]
    proposed = list(current)
    if recommendation and recommendation.get("product"):
        selected_id = recommendation["product"]["id"]
        for index, item in enumerate(products):
            if item["id"] == selected_id:
                proposed[index] = recommendation["proposed_price"]
                break
    return {"labels": labels, "current": current, "proposed": proposed}


def page_payload(selected_id: str = "", recommendation: dict | None = None) -> dict:
    products = list_products()
    if not selected_id and products:
        selected_id = products[0]["id"]
    selected = get_product(selected_id) if selected_id else None
    return {
        "products": products,
        "comparison": comparison_table(),
        "selected": selected,
        "selected_id": selected_id,
        "recommendation": recommendation,
        "model_status": MODEL_STATUS,
        "chart": chart_payload(recommendation),
    }


def _with_gaps(item: dict) -> dict:
    row = deepcopy(item)
    current = row["current_price"]
    competitor = row["competitor_price"]
    row["price_difference"] = round(current - competitor, 2)
    row["percent_difference"] = round((row["price_difference"] / competitor) * 100, 1) if competitor else None
    return row
