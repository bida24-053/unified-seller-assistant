"""In-memory demonstration dataset.

These records are synthetic. They are not Botswana seller performance
and must not be treated as a real customer extract.

Replace this module later with SQLAlchemy queries against a validated dataset.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date


# Research assumption displayed on the churn page. Not a validated rule.
CHURN_INACTIVITY_DAYS = 90
REFERENCE_DATE = date(2026, 10, 23)

SEGMENT_GUIDE = [
    {
        "id": "loyal",
        "label": "Loyal customers",
        "meaning": "Buy relatively often and have purchased recently. Demonstration label only.",
    },
    {
        "id": "high-value",
        "label": "High-value customers",
        "meaning": "Higher lifetime spend in the demonstration set. Demonstration label only.",
    },
    {
        "id": "new",
        "label": "New customers",
        "meaning": "Few purchases and a recent first or last order. Demonstration label only.",
    },
    {
        "id": "at-risk",
        "label": "At-risk customers",
        "meaning": "Previously active, but recency is slipping. Demonstration label only.",
    },
    {
        "id": "inactive",
        "label": "Inactive customers",
        "meaning": "Long gap since last purchase in the demonstration set. Demonstration label only.",
    },
]


def _base_customers() -> list[dict]:
    return [
        {
            "id": "C-1001",
            "name": "Demo Customer 01",
            "phone": "71 000 001",
            "location": "Gaborone",
            "last_purchase": date(2026, 10, 18),
            "order_count": 14,
            "total_spend": 4280.00,
            "segment": "loyal",
            "recency_days": 5,
            "frequency": 14,
            "monetary": 4280.00,
            "churn_risk": "low",
            "risk_notes": "Recent repeat purchases. Demonstration classification only.",
        },
        {
            "id": "C-1002",
            "name": "Demo Customer 02",
            "phone": "72 000 002",
            "location": "Francistown",
            "last_purchase": date(2026, 10, 12),
            "order_count": 9,
            "total_spend": 6120.50,
            "segment": "high-value",
            "recency_days": 11,
            "frequency": 9,
            "monetary": 6120.50,
            "churn_risk": "low",
            "risk_notes": "High spend with a recent order. Demonstration classification only.",
        },
        {
            "id": "C-1003",
            "name": "Demo Customer 03",
            "phone": "73 000 003",
            "location": "Maun",
            "last_purchase": date(2026, 10, 20),
            "order_count": 2,
            "total_spend": 340.00,
            "segment": "new",
            "recency_days": 3,
            "frequency": 2,
            "monetary": 340.00,
            "churn_risk": "medium",
            "risk_notes": "Short history; too few orders to judge retention. Demonstration classification only.",
        },
        {
            "id": "C-1004",
            "name": "Demo Customer 04",
            "phone": "74 000 004",
            "location": "Palapye",
            "last_purchase": date(2026, 8, 2),
            "order_count": 7,
            "total_spend": 1890.00,
            "segment": "at-risk",
            "recency_days": 82,
            "frequency": 7,
            "monetary": 1890.00,
            "churn_risk": "medium",
            "risk_notes": "Approaching the proposed 90-day inactivity window. Demonstration classification only.",
        },
        {
            "id": "C-1005",
            "name": "Demo Customer 05",
            "phone": "75 000 005",
            "location": "Molepolole",
            "last_purchase": date(2026, 4, 10),
            "order_count": 5,
            "total_spend": 970.00,
            "segment": "inactive",
            "recency_days": 196,
            "frequency": 5,
            "monetary": 970.00,
            "churn_risk": "high",
            "risk_notes": "No purchase within the proposed 90-day window. Demonstration classification only.",
        },
        {
            "id": "C-1006",
            "name": "Demo Customer 06",
            "phone": "76 000 006",
            "location": "Gaborone",
            "last_purchase": date(2026, 10, 8),
            "order_count": 11,
            "total_spend": 2550.75,
            "segment": "loyal",
            "recency_days": 15,
            "frequency": 11,
            "monetary": 2550.75,
            "churn_risk": "low",
            "risk_notes": "Regular cosmetics and hair-care orders. Demonstration classification only.",
        },
        {
            "id": "C-1007",
            "name": "Demo Customer 07",
            "phone": "77 000 007",
            "location": "Serowe",
            "last_purchase": date(2026, 9, 1),
            "order_count": 4,
            "total_spend": 760.00,
            "segment": "at-risk",
            "recency_days": 52,
            "frequency": 4,
            "monetary": 760.00,
            "churn_risk": "medium",
            "risk_notes": "Gap between orders is widening. Demonstration classification only.",
        },
        {
            "id": "C-1008",
            "name": "Demo Customer 08",
            "phone": "71 000 008",
            "location": "Lobatse",
            "last_purchase": date(2026, 3, 15),
            "order_count": 3,
            "total_spend": 410.00,
            "segment": "inactive",
            "recency_days": 222,
            "frequency": 3,
            "monetary": 410.00,
            "churn_risk": "high",
            "risk_notes": "Last order more than 90 days ago. Demonstration classification only.",
        },
        {
            "id": "C-1009",
            "name": "Demo Customer 09",
            "phone": "72 000 009",
            "location": "Gaborone",
            "last_purchase": date(2026, 10, 21),
            "order_count": 1,
            "total_spend": 185.00,
            "segment": "new",
            "recency_days": 2,
            "frequency": 1,
            "monetary": 185.00,
            "churn_risk": "medium",
            "risk_notes": "Single demonstration purchase only. Demonstration classification only.",
        },
        {
            "id": "C-1010",
            "name": "Demo Customer 10",
            "phone": "73 000 010",
            "location": "Kasane",
            "last_purchase": date(2026, 10, 5),
            "order_count": 8,
            "total_spend": 7340.00,
            "segment": "high-value",
            "recency_days": 18,
            "frequency": 8,
            "monetary": 7340.00,
            "churn_risk": "low",
            "risk_notes": "High basket values on electronics accessories. Demonstration classification only.",
        },
        {
            "id": "C-1011",
            "name": "Demo Customer 11",
            "phone": "74 000 011",
            "location": "Mahalapye",
            "last_purchase": date(2026, 6, 20),
            "order_count": 6,
            "total_spend": 1120.00,
            "segment": "inactive",
            "recency_days": 125,
            "frequency": 6,
            "monetary": 1120.00,
            "churn_risk": "high",
            "risk_notes": "No recent airtime or grocery restock. Demonstration classification only.",
        },
        {
            "id": "C-1012",
            "name": "Demo Customer 12",
            "phone": "75 000 012",
            "location": "Gaborone",
            "last_purchase": date(2026, 10, 14),
            "order_count": 10,
            "total_spend": 3015.25,
            "segment": "loyal",
            "recency_days": 9,
            "frequency": 10,
            "monetary": 3015.25,
            "churn_risk": "low",
            "risk_notes": "Steady clothing and household orders. Demonstration classification only.",
        },
    ]


def _base_transactions() -> list[dict]:
    return [
        {"id": "T-1041", "customer_id": "C-1001", "product": "Hair oil 100ml", "category": "Hair care", "purchase_date": date(2026, 10, 18), "value": 85.00},
        {"id": "T-1040", "customer_id": "C-1009", "product": "Lip gloss set", "category": "Cosmetics", "purchase_date": date(2026, 10, 21), "value": 185.00},
        {"id": "T-1039", "customer_id": "C-1003", "product": "Airtime P50", "category": "Airtime", "purchase_date": date(2026, 10, 20), "value": 50.00},
        {"id": "T-1038", "customer_id": "C-1012", "product": "Ladies blouse", "category": "Clothing", "purchase_date": date(2026, 10, 14), "value": 220.00},
        {"id": "T-1037", "customer_id": "C-1002", "product": "Phone charger", "category": "Electronics accessories", "purchase_date": date(2026, 10, 12), "value": 150.00},
        {"id": "T-1036", "customer_id": "C-1006", "product": "Body lotion", "category": "Cosmetics", "purchase_date": date(2026, 10, 8), "value": 95.00},
        {"id": "T-1035", "customer_id": "C-1010", "product": "Wireless earbuds", "category": "Electronics accessories", "purchase_date": date(2026, 10, 5), "value": 890.00},
        {"id": "T-1034", "customer_id": "C-1001", "product": "Maize meal 10kg", "category": "Groceries", "purchase_date": date(2026, 10, 1), "value": 89.95},
        {"id": "T-1033", "customer_id": "C-1007", "product": "Airtime P100", "category": "Airtime", "purchase_date": date(2026, 9, 1), "value": 100.00},
        {"id": "T-1032", "customer_id": "C-1004", "product": "School shoes", "category": "Clothing", "purchase_date": date(2026, 8, 2), "value": 320.00},
        {"id": "T-1031", "customer_id": "C-1012", "product": "Kitchen towel pack", "category": "Household", "purchase_date": date(2026, 9, 20), "value": 75.00},
        {"id": "T-1030", "customer_id": "C-1002", "product": "Bluetooth speaker", "category": "Electronics accessories", "purchase_date": date(2026, 9, 15), "value": 450.00},
        {"id": "T-1029", "customer_id": "C-1006", "product": "Relaxer kit", "category": "Hair care", "purchase_date": date(2026, 9, 10), "value": 140.00},
        {"id": "T-1028", "customer_id": "C-1011", "product": "Cooking oil 2L", "category": "Groceries", "purchase_date": date(2026, 6, 20), "value": 65.00},
        {"id": "T-1027", "customer_id": "C-1005", "product": "Airtime P30", "category": "Airtime", "purchase_date": date(2026, 4, 10), "value": 30.00},
        {"id": "T-1026", "customer_id": "C-1008", "product": "T-shirt", "category": "Clothing", "purchase_date": date(2026, 3, 15), "value": 120.00},
        {"id": "T-1025", "customer_id": "C-1010", "product": "Power bank", "category": "Electronics accessories", "purchase_date": date(2026, 8, 22), "value": 280.00},
        {"id": "T-1024", "customer_id": "C-1001", "product": "Body lotion", "category": "Cosmetics", "purchase_date": date(2026, 9, 5), "value": 95.00},
        {"id": "T-1023", "customer_id": "C-1003", "product": "Snack pack", "category": "Groceries", "purchase_date": date(2026, 10, 4), "value": 45.00},
        {"id": "T-1022", "customer_id": "C-1012", "product": "Airtime P50", "category": "Airtime", "purchase_date": date(2026, 8, 30), "value": 50.00},
        {"id": "T-1021", "customer_id": "C-1002", "product": "Hair oil 100ml", "category": "Hair care", "purchase_date": date(2026, 7, 18), "value": 85.00},
        {"id": "T-1020", "customer_id": "C-1006", "product": "Lip gloss set", "category": "Cosmetics", "purchase_date": date(2026, 8, 12), "value": 185.00},
    ]


def _base_products() -> list[dict]:
    return [
        {
            "id": "P-01",
            "name": "Hair oil 100ml",
            "category": "Hair care",
            "current_price": 85.00,
            "cost": 42.00,
            "competitor_price": 79.00,
        },
        {
            "id": "P-02",
            "name": "Lip gloss set",
            "category": "Cosmetics",
            "current_price": 185.00,
            "cost": 95.00,
            "competitor_price": 199.00,
        },
        {
            "id": "P-03",
            "name": "Airtime P50",
            "category": "Airtime",
            "current_price": 50.00,
            "cost": 48.50,
            "competitor_price": 50.00,
        },
        {
            "id": "P-04",
            "name": "Ladies blouse",
            "category": "Clothing",
            "current_price": 220.00,
            "cost": 110.00,
            "competitor_price": 195.00,
        },
        {
            "id": "P-05",
            "name": "Wireless earbuds",
            "category": "Electronics accessories",
            "current_price": 890.00,
            "cost": 520.00,
            "competitor_price": 849.00,
        },
        {
            "id": "P-06",
            "name": "Maize meal 10kg",
            "category": "Groceries",
            "current_price": 89.95,
            "cost": 72.00,
            "competitor_price": 92.50,
        },
    ]


def _base_sales_trend() -> list[dict]:
    return [
        {"month": "Apr 2026", "revenue": 980.00},
        {"month": "May 2026", "revenue": 1240.00},
        {"month": "Jun 2026", "revenue": 1115.00},
        {"month": "Jul 2026", "revenue": 1680.00},
        {"month": "Aug 2026", "revenue": 1540.00},
        {"month": "Sep 2026", "revenue": 1895.00},
        {"month": "Oct 2026", "revenue": 2210.00},
    ]


class DemoStore:
    """Process-memory store. Data is lost when the Flask process stops."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.customers = _base_customers()
        self.transactions = _base_transactions()
        self.products = _base_products()
        self.sales_trend = _base_sales_trend()
        self.churn_inactivity_days = CHURN_INACTIVITY_DAYS
        self.reference_date = REFERENCE_DATE
        self.segment_guide = deepcopy(SEGMENT_GUIDE)
        self._next_customer = 1013

    def next_customer_id(self) -> str:
        customer_id = f"C-{self._next_customer:04d}"
        self._next_customer += 1
        return customer_id


store = DemoStore()
