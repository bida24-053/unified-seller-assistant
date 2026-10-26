"""RFM scoring and presentation helpers.

Segments are calculated from demonstration recency, frequency and monetary
values. Replace assign_segments() later with a validated research algorithm.
"""

from __future__ import annotations

from src.services.customer_service import SEGMENT_LABELS, list_customers
from src.services.demo_data import store

EXPLAINERS = {
    "recency": (
        "How recently the customer last purchased, counted in days from the "
        "demonstration reference date. A smaller number means a more recent order."
    ),
    "frequency": (
        "How many orders the customer has placed in the demonstration history. "
        "A larger number means more repeat purchasing."
    ),
    "monetary": (
        "How much the customer has spent in Botswana pula. A larger number "
        "means higher lifetime value in this demonstration set."
    ),
}

NOT_EVALUATED = "Not evaluated"


def assign_segments(customers: list[dict] | None = None) -> list[dict]:
    """Assign RFM scores (1-5) and a provisional segment to each customer."""
    records = [dict(item) for item in (customers if customers is not None else list_customers())]
    if not records:
        return records

    recency_values = [item["recency_days"] for item in records]
    frequency_values = [item["frequency"] for item in records]
    monetary_values = [item["monetary"] for item in records]

    recency_scores = _score_values(recency_values, higher_is_better=False)
    frequency_scores = _score_values(frequency_values, higher_is_better=True)
    monetary_scores = _score_values(monetary_values, higher_is_better=True)

    for item, recency_score, frequency_score, monetary_score in zip(
        records, recency_scores, frequency_scores, monetary_scores
    ):
        item["r_score"] = recency_score
        item["f_score"] = frequency_score
        item["m_score"] = monetary_score
        item["calculated_segment"] = _segment_from_scores(
            item, recency_score, frequency_score, monetary_score
        )
        item["segment_label"] = SEGMENT_LABELS.get(item["segment"], item["segment"])
    return records


def page_payload(query: str = "", segment: str = "") -> dict:
    scored = assign_segments()
    cards = _cards(scored)
    rows = scored
    query = (query or "").strip().lower()
    segment = (segment or "").strip()
    if query:
        rows = [
            item
            for item in rows
            if query in item["id"].lower() or query in item["name"].lower()
        ]
    if segment:
        rows = [item for item in rows if item["segment"] == segment]
    rows.sort(key=lambda item: item["id"])
    return {
        "explainers": EXPLAINERS,
        "cards": cards,
        "segments": store.segment_guide,
        "rows": rows,
        "chart": {
            "labels": [card["label"] for card in cards],
            "values": [card["count"] for card in cards],
        },
        "query": query,
        "segment": segment,
        "model_status": (
            "RFM scores are calculated from demonstration recency, frequency and "
            "monetary values. This is not a trained machine-learning model."
        ),
        "accuracy": NOT_EVALUATED,
        "precision": NOT_EVALUATED,
        "recall": NOT_EVALUATED,
        "f1": NOT_EVALUATED,
    }


def segment_counts() -> list[dict]:
    scored = assign_segments()
    return _cards(scored)


def rfm_table(query: str = "", segment: str = "") -> list[dict]:
    return page_payload(query=query, segment=segment)["rows"]


def _cards(customers: list[dict]) -> list[dict]:
    counts: dict[str, int] = {key: 0 for key in SEGMENT_LABELS}
    for item in customers:
        counts[item["segment"]] = counts.get(item["segment"], 0) + 1
    return [
        {
            "id": item["id"],
            "label": item["label"],
            "description": item["meaning"],
            "meaning": item["meaning"],
            "count": counts.get(item["id"], 0),
        }
        for item in store.segment_guide
    ]


def _score_values(values: list[int] | list[float], higher_is_better: bool) -> list[int]:
    """Map values to 1-5 ranks. Ties share the same score."""
    unique = sorted(set(values), reverse=higher_is_better)
    if len(unique) == 1:
        return [3 for _ in values]
    buckets = max(len(unique) - 1, 1)
    lookup = {}
    for index, value in enumerate(unique):
        lookup[value] = 5 - round(index * 4 / buckets)
    return [int(lookup[value]) for value in values]


def _segment_from_scores(item: dict, recency_score: int, frequency_score: int, monetary_score: int) -> str:
    recency_days = item["recency_days"]
    frequency = item["frequency"]
    if recency_days >= store.churn_inactivity_days:
        return "inactive"
    if frequency <= 2 and recency_days <= 21:
        return "new"
    if monetary_score >= 4 and frequency_score >= 3:
        return "high-value"
    if recency_days >= 45:
        return "at-risk"
    if recency_score >= 4 and frequency_score >= 4:
        return "loyal"
    if frequency_score >= 4:
        return "loyal"
    if recency_days >= 30:
        return "at-risk"
    return "loyal"
