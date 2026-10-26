"""Unified Seller CRM and Pricing Assistant — front-end prototype."""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from src.services import churn_service, customer_service, metrics_service, pricing_service, rfm_service
from src.services.customer_service import SEGMENT_LABELS
from src.services.demo_data import store

ROOT = Path(__file__).resolve().parent


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(ROOT / "templates"),
        static_folder=str(ROOT / "static"),
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-prototype-not-for-production")
    app.config["DEMO_MODE"] = True

    @app.context_processor
    def inject_globals():
        return {
            "app_name": "Unified Seller Assistant",
            "app_short": "USA",
            "demo_mode": True,
            "nav_items": [
                {"endpoint": "dashboard", "label": "Dashboard", "icon": "bi-speedometer2"},
                {"endpoint": "customers", "label": "Customers", "icon": "bi-people"},
                {"endpoint": "segmentation", "label": "RFM Segmentation", "icon": "bi-diagram-3"},
                {"endpoint": "churn", "label": "Churn Risk", "icon": "bi-exclamation-triangle"},
                {"endpoint": "pricing", "label": "Pricing Assistant", "icon": "bi-tag"},
                {"endpoint": "about", "label": "About", "icon": "bi-info-circle"},
            ],
            "segment_labels": SEGMENT_LABELS,
        }

    @app.template_filter("pula")
    def pula_filter(value) -> str:
        try:
            amount = float(value)
        except (TypeError, ValueError):
            return "P0.00"
        return f"P{amount:,.2f}"

    @app.template_filter("display_date")
    def display_date_filter(value) -> str:
        if value is None or value == "":
            return "—"
        if isinstance(value, datetime):
            return value.strftime("%d %b %Y")
        if isinstance(value, date):
            return value.strftime("%d %b %Y")
        return str(value)

    @app.route("/")
    def dashboard():
        metrics = metrics_service.dashboard(
            date_from=request.args.get("date_from", ""),
            date_to=request.args.get("date_to", ""),
        )
        return render_template("dashboard.html", metrics=metrics)

    @app.route("/customers", methods=["GET", "POST"])
    def customers():
        form_values = {
            "name": "",
            "location": "",
            "phone": "",
            "last_purchase": "",
            "order_count": "1",
            "total_spend": "0",
            "segment": "new",
        }
        if request.method == "POST":
            form_values.update({key: request.form.get(key, "") for key in form_values})
            payload, errors = customer_service.validate_new_customer(request.form)
            if errors:
                for error in errors:
                    flash(error, "danger")
            else:
                record = customer_service.add_customer(payload)
                flash(
                    (
                        f"{record['name']} was added to the in-memory demonstration list "
                        f"as {record['id']}. It will disappear when the application restarts."
                    ),
                    "success",
                )
                return redirect(url_for("customer_detail", customer_id=record["id"]))

        query = request.args.get("q", "")
        segment = request.args.get("segment", "")
        records = customer_service.list_customers(query=query, segment=segment)
        return render_template(
            "customers.html",
            customers=records,
            query=query,
            segment=segment,
            form_values=form_values,
        )

    @app.route("/customers/<customer_id>")
    def customer_detail(customer_id: str):
        record = customer_service.get_customer(customer_id)
        if record is None:
            flash("That demonstration customer was not found.", "danger")
            return redirect(url_for("customers"))
        return render_template(
            "customer_detail.html",
            customer=record,
            transactions=record["transactions"],
        )

    @app.route("/segmentation")
    def segmentation():
        payload = rfm_service.page_payload(
            query=request.args.get("q", ""),
            segment=request.args.get("segment", ""),
        )
        return render_template("segmentation.html", **payload)

    @app.route("/churn")
    def churn():
        payload = churn_service.page_payload(
            query=request.args.get("q", ""),
            risk=request.args.get("risk", ""),
        )
        return render_template("churn.html", **payload)

    @app.route("/pricing", methods=["GET", "POST"])
    def pricing():
        recommendation = None
        selected_id = request.form.get("product_id") or request.args.get("product_id") or ""
        if request.method == "POST":
            recommendation = pricing_service.generate_recommendation(selected_id)
            if recommendation.get("error"):
                flash(recommendation["error"], "danger")
                recommendation = None
            else:
                flash("Demonstration recommendation generated. No selling price was changed.", "info")
        payload = pricing_service.page_payload(selected_id=selected_id, recommendation=recommendation)
        return render_template("pricing.html", **payload)

    @app.route("/about")
    def about():
        return render_template("about.html", customer_count=len(store.customers))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
