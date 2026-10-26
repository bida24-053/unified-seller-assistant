"""Customer directory operations.

In-memory only. Swap this module for SQLAlchemy persistence later.
"""

from __future__ import annotations

from datetime import date, datetime

from src.services.demo_data import store


SEGMENT_LABELS = {
    "loyal": "Loyal customers",
    "high-value": "High-value customers",
    "new": "New customers",
    "at-risk": "At-risk customers",
    "inactive": "Inactive customers",
}

VALID_SEGMENTS = set(SEGMENT_LABELS)


def decorate(item: dict) -> dict:
    record = dict(item)
    record["segment_label"] = SEGMENT_LABELS.get(record.get("segment", ""), record.get("segment", ""))
    return record


def list_customers(query: str = "", segment: str = "") -> list[dict]:
    records = [decorate(item) for item in store.customers]
    query = (query or "").strip().lower()
    segment = (segment or "").strip()
    if query:
        records = [
            item
            for item in records
            if query in item["id"].lower() or query in item["name"].lower()
        ]
    if segment:
        records = [item for item in records if item["segment"] == segment]
    records.sort(key=lambda item: item["id"])
    return records


def get_customer(customer_id: str) -> dict | None:
    for item in store.customers:
        if item["id"] == customer_id:
            record = decorate(item)
            record["transactions"] = customer_transactions(customer_id)
            return record
    return None


def customer_transactions(customer_id: str) -> list[dict]:
    rows = [dict(item) for item in store.transactions if item["customer_id"] == customer_id]
    rows.sort(key=lambda item: item["purchase_date"], reverse=True)
    return rows


def validate_new_customer(form: dict) -> tuple[dict, list[str]]:
    errors: list[str] = []
    name = (form.get("name") or "").strip()
    location = (form.get("location") or "").strip()
    phone = (form.get("phone") or "").strip()
    segment = (form.get("segment") or "").strip()
    last_purchase_raw = (form.get("last_purchase") or "").strip()
    order_count_raw = (form.get("order_count") or "").strip()
    total_spend_raw = (form.get("total_spend") or "").strip()

    if not name or len(name) < 2:
        if not name:
            errors.append("Customer name is required.")
        errors.append("Customer name must be at least 2 characters.")
        errors.append("Please correct the highlighted fields.")

    last_purchase = store.reference_date
    if last_purchase_raw:
        try:
            last_purchase = datetime.strptime(last_purchase_raw, "%Y-%m-%d").date()
        except ValueError:
            last_purchase = None
            errors.append("Last purchase date must use YYYY-MM-DD.")
        else:
            if last_purchase > date.today():
                errors.append("Last purchase date cannot be in the future.")

    if order_count_raw == "":
        order_count = 1
    else:
        try:
            order_count = int(order_count_raw)
            if order_count < 0:
                errors.append("Number of orders cannot be negative.")
        except ValueError:
            order_count = 0
            errors.append("Number of orders must be a whole number.")

    if total_spend_raw == "":
        total_spend = 0.0
    else:
        try:
            total_spend = float(total_spend_raw)
            if total_spend < 0:
                errors.append("Total spending cannot be negative.")
        except ValueError:
            total_spend = 0.0
            errors.append("Total spending must be a number in Botswana pula.")

    if not segment:
        errors.append("Select a demonstration customer segment.")
        if "Please correct the highlighted fields." not in errors:
            errors.append("Please correct the highlighted fields.")
    elif segment not in VALID_SEGMENTS:
        errors.append("Select a demonstration customer segment.")

    payload = {
        "name": name,
        "location": location or "Not provided",
        "phone": phone,
        "segment": segment or "new",
        "last_purchase": last_purchase or store.reference_date,
        "order_count": order_count,
        "total_spend": round(total_spend, 2),
    }
    return payload, errors


def add_customer(payload: dict) -> dict:
    recency = (store.reference_date - payload["last_purchase"]).days
    if recency < 0:
        recency = 0
    if recency >= store.churn_inactivity_days:
        churn_risk = "high"
    elif recency >= 45:
        churn_risk = "medium"
    else:
        churn_risk = "low"

    record = {
        "id": store.next_customer_id(),
        "name": payload["name"],
        "phone": payload["phone"] or "Not provided",
        "location": payload["location"],
        "last_purchase": payload["last_purchase"],
        "order_count": payload["order_count"],
        "total_spend": payload["total_spend"],
        "segment": payload["segment"],
        "recency_days": recency,
        "frequency": payload["order_count"],
        "monetary": payload["total_spend"],
        "churn_risk": churn_risk,
        "risk_notes": "Added in this session as demonstration data. Not saved to a database.",
    }
    store.customers.append(record)
    return decorate(record)
