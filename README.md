# Unified Seller CRM and Pricing Assistant

Front-end prototype for a Botswana Accountancy College Research and Innovation project.

The application helps informal online sellers and small businesses in Botswana explore customer records, purchasing behaviour, inactivity risk and advisory pricing in one interface. This repository currently delivers the **user interface, navigation and demonstration interactions**. A database and machine-learning models are not connected yet.

This is a student research prototype, not a commercial product.

## Research purpose

Small online sellers often keep customer and sales information in fragmented tools. The research explores a unified system that combines:

- Customer Relationship Management (CRM)
- Recency, Frequency and Monetary value (RFM) segmentation
- Machine-learning customer churn prediction
- Explainable pricing recommendations
- An integrated dashboard

Currency is shown in Botswana pula (P). All sample records are synthetic demonstration data.

## Main application features (this prototype)

| Page | Route | What works now |
| --- | --- | --- |
| Dashboard | `/` | Summary cards, Chart.js visuals, date filter, recent transactions |
| Customers | `/customers` | Search, segment filter, add-customer form with validation, detail view |
| RFM segmentation | `/segmentation` | Segment explanations, cards, chart and filterable table |
| Churn prediction | `/churn` | Risk table, 90-day research assumption, honest “model not connected” message |
| Pricing assistant | `/pricing` | Product comparison, advisory demonstration recommendation |
| About | `/about` | Project context, status and limitations |

Customer records added in the form are held **in memory only**. They disappear when the server stops.

## Technology stack

- Python 3.12
- Flask and Jinja templates
- HTML5, CSS3, JavaScript
- Bootstrap 5 and Bootstrap Icons
- Chart.js
- pytest

React, Node.js and Docker are not used.

## Project folder structure

```text
unified-seller-assistant/
  app.py                 Flask application factory and routes
  requirements.txt
  README.md
  .gitignore
  .env.example
  pytest.ini
  templates/             Shared layout and page templates
  static/css/style.css
  static/js/main.js      Sidebar behaviour
  static/js/charts.js    Chart.js configuration
  src/services/          Isolated demonstration data and future model hooks
  tests/test_app.py
```

The extra service modules (`customer_service.py`, `rfm_service.py`, `churn_service.py`, `pricing_service.py`, `metrics_service.py`) keep HTML templates free of business logic so SQLAlchemy and Scikit-learn can replace the demonstration layer later. `customer_detail.html` was added for the customer details view.

## Installation

1. Install Python 3.12 if it is not already installed.
2. Open a terminal in this folder.

### Windows PowerShell — virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py` is unavailable, use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to run the application

With the virtual environment activated:

```powershell
python app.py
```

Then open http://127.0.0.1:5000 in a browser.

## Deploy to Render

The repository includes a Render Blueprint configuration in `render.yaml`.

1. Sign in to [Render](https://render.com/) and choose **New > Blueprint**.
2. Connect the `bida24-053/unified-seller-assistant` GitHub repository and select the `main` branch.
3. Review and deploy the `unified-seller-assistant` web service. Render installs the dependencies and generates a production `SECRET_KEY` automatically.
4. When deployment finishes, open the `onrender.com` URL shown in the Render dashboard. Share that live URL to let others use the frontend.

The free web service may take a short time to wake up after inactivity. Customer additions remain in memory and reset when the service restarts.

## How to run tests

```powershell
pytest -q
```

## Current limitations

- Demonstration data only; not actual seller performance.
- No SQL database. Added customers are not permanently saved.
- No trained RFM algorithm, churn classifier or pricing regression model.
- No real accuracy, precision, recall, F1-score or ROC-AUC figures are shown because no model has been evaluated.
- Pricing suggestions are a labelled demonstration heuristic and remain advisory.

## Features still awaiting integration

- SQLAlchemy and a SQL database
- Data validation and cleaning for a research dataset
- RFM calculation from real transactions
- Logistic regression and decision-tree churn predictions
- Linear regression or decision-tree pricing recommendations, subject to the validated target variable

Do not commit confidential customer files, `.env` secrets, local databases or trained model artefacts. `.gitignore` is configured to exclude those paths.

## Supervisor progress summary

1. **Front-end pages implemented:** Dashboard, Customers (including details), RFM Segmentation, Churn Risk, Pricing Assistant, About — with shared sidebar, top bar and responsive layout.
2. **Interactions that work:** Navigation, dashboard date filter, customer search/filter, validated add-customer form, RFM and churn filters, pricing “Generate Recommendation” button, Chart.js charts fed from demonstration JSON.
3. **Tests performed:** pytest coverage of the six routes, navigation, search/filter, form validation, in-memory create, churn/pricing honesty messages, and empty date-filter state. Flask startup is verified separately after install.
4. **Not yet implemented:** Database persistence and all machine-learning components.
