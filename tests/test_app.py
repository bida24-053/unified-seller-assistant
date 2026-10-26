from src.services.demo_data import store


def test_all_primary_routes_succeed(client):
    for path in ["/", "/customers", "/segmentation", "/churn", "/pricing", "/about"]:
        response = client.get(path)
        assert response.status_code == 200, path


NAV_PATHS = ["/", "/customers", "/segmentation", "/churn", "/pricing", "/about"]
NAV_LABELS = [
    "Dashboard",
    "Customers",
    "RFM Segmentation",
    "Churn Risk",
    "Pricing Assistant",
    "About",
]


def test_navigation_links_use_internal_routes(client):
    for path in NAV_PATHS + ["/customers/C-1001"]:
        response = client.get(path)
        assert response.status_code == 200, path
        html = response.get_data(as_text=True)
        for href in ["/customers", "/segmentation", "/churn", "/pricing", "/about"]:
            assert f'href="{href}"' in html
        for label in NAV_LABELS:
            assert label in html


def test_dashboard_contains_demo_label_and_charts(client):
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert "demonstration data" in html.lower()
    assert "salesTrendChart" in html
    assert "dashboard-chart-data" in html


def test_demo_dataset_includes_50_additional_customers_with_linked_transactions(client):
    assert len(store.customers) == 62
    assert len({item["id"] for item in store.customers}) == 62
    assert len(store.transactions) == 72

    added_customers = [item for item in store.customers if item["id"] >= "C-1013"]
    assert len(added_customers) == 50
    assert {item["segment"] for item in added_customers} == {
        "loyal",
        "high-value",
        "new",
        "at-risk",
        "inactive",
    }
    assert all(
        any(transaction["customer_id"] == customer["id"] for transaction in store.transactions)
        for customer in added_customers
    )

    response = client.get("/customers/C-1013")
    assert response.status_code == 200
    assert "Demo Customer 13" in response.get_data(as_text=True)


def test_dashboard_date_filter_can_empty_transactions(client):
    response = client.get("/?date_from=2010-01-01&date_to=2010-01-02")
    html = response.get_data(as_text=True)
    assert "No demonstration transactions match the selected dates." in html


def test_customer_search_and_segment_filter(client):
    search = client.get("/customers?q=C-1001")
    search_html = search.get_data(as_text=True)
    assert "C-1001" in search_html
    assert "C-1002" not in search_html

    filtered = client.get("/customers?segment=inactive")
    filtered_html = filtered.get_data(as_text=True)
    assert "C-1005" in filtered_html
    assert "C-1001" not in filtered_html


def test_customer_form_requires_name_and_segment(client):
    response = client.post("/customers", data={"name": "", "segment": ""}, follow_redirects=True)
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Please correct the highlighted fields" in html
    assert "at least 2 characters" in html


def test_customer_add_is_in_memory_only(client):
    before = len(store.customers)
    response = client.post(
        "/customers",
        data={
            "name": "Demo Customer Extra",
            "segment": "new",
            "order_count": "1",
            "total_spend": "50",
        },
        follow_redirects=True,
    )
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Demo Customer Extra" in html
    assert "in-memory demonstration list" in html
    assert len(store.customers) == before + 1
    assert store.customers[-1]["id"] == "C-1063"


def test_unknown_customer_redirects(client):
    response = client.get("/customers/does-not-exist", follow_redirects=True)
    assert response.status_code == 200
    assert "was not found" in response.get_data(as_text=True)


def test_segmentation_and_churn_filters(client):
    segment_page = client.get("/segmentation?segment=loyal&q=C-1001")
    assert segment_page.status_code == 200
    html = segment_page.get_data(as_text=True)
    assert "C-1001" in html
    assert "Provisional demonstration" in html or "provisional demonstration" in html.lower()

    churn_page = client.get("/churn?risk=high")
    churn_html = churn_page.get_data(as_text=True)
    assert churn_page.status_code == 200
    assert "Machine-learning model not yet connected" in churn_html
    assert "C-1005" in churn_html
    assert "configurable research assumption" in churn_html.lower() or "research assumption" in churn_html.lower()


def test_pricing_requires_product_and_generates_demo_recommendation(client):
    missing = client.post("/pricing", data={"product_id": ""}, follow_redirects=True)
    assert "Select a product" in missing.get_data(as_text=True)

    created = client.post("/pricing", data={"product_id": "P-01"}, follow_redirects=True)
    html = created.get_data(as_text=True)
    assert created.status_code == 200
    assert "Demonstration heuristic" in html
    assert "not a model prediction" in html.lower()
    assert "Proposed selling price" in html
