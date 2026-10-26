"""Dashboard aggregates built from the demonstration store."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from src.services.churn_service import risk_counts
from src.services.customer_service import list_customers
from src.services.demo_data import store
from src.services.rfm_service import segment_counts


def dashboard(date_from: str = "", date_to: str = "") -> dict:
    transactions = [dict(item) for item in store.transactions]
    parsed_from = _parse_date(date_from)
    parsed_to = _parse_date(date_to)
    if parsed_from:
        transactions = [item for item in transactions if item["purchase_date"] >= parsed_from]
    if parsed_to:
        transactions = [item for item in transactions if item["purchase_date"] <= parsed_to]

    customers = list_customers()
    at_risk = [
        item
        for item in customers
        if item["segment"] in {"at-risk", "inactive"} or item["churn_risk"] == "high"
    ]
    revenue = sum(item["value"] for item in transactions)

    categories: dict[str, float] = defaultdict(float)
    for item in transactions:
        categories[item["category"]] += item["value"]

    recent = sorted(transactions, key=lambda item: item["purchase_date"], reverse=True)[:8]
    segments = segment_counts()
    churn = risk_counts()
    sales_trend = list(store.sales_trend)

    return {
        "total_customers": len(customers),
        "total_transactions": len(transactions),
        "total_revenue": round(revenue, 2),
        "at_risk_count": len(at_risk),
        "sales_trend": sales_trend,
        "segment_counts": segments,
        "category_sales": [{"category": key, "value": round(value, 2)} for key, value in categories.items()],
        "churn_counts": churn,
        "recent_transactions": recent,
        "date_from": date_from,
        "date_to": date_to,
        "is_filtered": bool(parsed_from or parsed_to),
        "chart": {
            "sales_trend": {
                "labels": [item["month"] for item in sales_trend],
                "values": [item["revenue"] for item in sales_trend],
            },
            "rfm": {
                "labels": [item["label"] for item in segments],
                "values": [item["count"] for item in segments],
            },
            "categories": {
                "labels": list(categories.keys()),
                "values": [round(value, 2) for value in categories.values()],
            },
            "churn": {
                "labels": ["High", "Medium", "Low"],
                "values": [churn["high"], churn["medium"], churn["low"]],
            },
        },
    }


def _parse_date(value: str):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None
