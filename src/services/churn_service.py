"""Churn-risk presentation helpers.

Replace model_performance() later with logistic regression and decision-tree
predictions. This prototype does not invent classifier scores.
"""

from __future__ import annotations

from src.services.customer_service import list_customers
from src.services.demo_data import store

MODEL_STATUS = (
    "Machine-learning model not yet connected. Demonstration records are shown "
    "for interface development."
)
NOT_EVALUATED = "Not evaluated"


def risk_counts() -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for item in list_customers():
        counts[item["churn_risk"]] = counts.get(item["churn_risk"], 0) + 1
    return counts


def list_risks(query: str = "", risk: str = "") -> list[dict]:
    records = list_customers(query=query)
    decorated = []
    for item in records:
        row = dict(item)
        recency = row.get("recency_days")
        row["beyond_window"] = recency is not None and recency >= store.churn_inactivity_days
        decorated.append(row)
    if risk:
        decorated = [item for item in decorated if item["churn_risk"] == risk]
    return decorated


def research_assumption() -> dict:
    return {
        "inactivity_days": store.churn_inactivity_days,
        "window_days": store.churn_inactivity_days,
        "reference_date": store.reference_date,
        "statement": (
            f"Proposed research assumption: a customer is treated as churned if "
            f"there is no purchase within {store.churn_inactivity_days} days. "
            "This rule is subject to validation against the dataset purchasing cycle."
        ),
        "definition": (
            f"Proposed research assumption: a customer is treated as churned if "
            f"there is no purchase within {store.churn_inactivity_days} days. "
            "This rule is subject to validation against the dataset purchasing cycle."
        ),
        "model_status": MODEL_STATUS,
    }


def model_performance() -> dict:
    metrics = _fit_demonstration_classifiers()
    return {
        "status": metrics.get("status", MODEL_STATUS),
        "logistic_regression": metrics.get("logistic_regression", "Not connected"),
        "decision_tree": metrics.get("decision_tree", "Not connected"),
        "accuracy": metrics.get("accuracy", NOT_EVALUATED),
        "precision": metrics.get("precision", NOT_EVALUATED),
        "recall": metrics.get("recall", NOT_EVALUATED),
        "f1": metrics.get("f1", NOT_EVALUATED),
        "roc_auc": metrics.get("roc_auc", NOT_EVALUATED),
    }


def page_payload(query: str = "", risk: str = "") -> dict:
    rows = list_risks(query=query, risk=risk)
    counts = risk_counts()
    return {
        "assumption": research_assumption(),
        "model": model_performance(),
        "risk_counts": counts,
        "rows": rows,
        "query": query,
        "risk": risk,
        "chart": {
            "labels": ["High", "Medium", "Low"],
            "values": [counts["high"], counts["medium"], counts["low"]],
        },
    }


def _fit_demonstration_classifiers() -> dict:
    """Placeholder until validated logistic regression and decision-tree models exist."""
    return {
        "status": MODEL_STATUS,
        "logistic_regression": "Not connected",
        "decision_tree": "Not connected",
        "accuracy": NOT_EVALUATED,
        "precision": NOT_EVALUATED,
        "recall": NOT_EVALUATED,
        "f1": NOT_EVALUATED,
        "roc_auc": NOT_EVALUATED,
    }
