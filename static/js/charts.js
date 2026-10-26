(function () {
  const teal = "#1a9b8a";
  const navy = "#0b1f3a";
  const gold = "#d97706";
  const rust = "#b42318";
  const slate = "#5b6b80";
  const palette = [teal, navy, gold, rust, slate, "#3b82f6"];

  function readJson(id) {
    const node = document.getElementById(id);
    if (!node) {
      return null;
    }
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      console.error("Could not parse chart data for", id, error);
      return null;
    }
  }

  function makeChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === "undefined") {
      return;
    }
    new Chart(canvas, config);
  }

  const dashboard = readJson("dashboard-chart-data");
  if (dashboard) {
    makeChart("salesTrendChart", {
      type: "line",
      data: {
        labels: dashboard.sales_trend.labels,
        datasets: [{
          label: "Demonstration revenue (P)",
          data: dashboard.sales_trend.values,
          borderColor: teal,
          backgroundColor: "rgba(26, 155, 138, 0.15)",
          fill: true,
          tension: 0.3,
        }],
      },
      options: { responsive: true, plugins: { legend: { display: false } } },
    });

    makeChart("rfmChart", {
      type: "doughnut",
      data: {
        labels: dashboard.rfm.labels,
        datasets: [{ data: dashboard.rfm.values, backgroundColor: palette }],
      },
      options: { responsive: true, plugins: { legend: { position: "bottom" } } },
    });

    makeChart("categoryChart", {
      type: "bar",
      data: {
        labels: dashboard.categories.labels,
        datasets: [{
          label: "Demonstration sales (P)",
          data: dashboard.categories.values,
          backgroundColor: navy,
        }],
      },
      options: { responsive: true, plugins: { legend: { display: false } } },
    });

    makeChart("churnChart", {
      type: "bar",
      data: {
        labels: dashboard.churn.labels,
        datasets: [{
          label: "Demonstration customers",
          data: dashboard.churn.values,
          backgroundColor: [rust, gold, teal],
        }],
      },
      options: { responsive: true, plugins: { legend: { display: false } } },
    });
  }

  const segments = readJson("segment-chart-data");
  if (segments) {
    makeChart("segmentChart", {
      type: "doughnut",
      data: {
        labels: segments.labels,
        datasets: [{ data: segments.values, backgroundColor: palette }],
      },
      options: { responsive: true, plugins: { legend: { position: "bottom" } } },
    });
  }

  const churn = readJson("churn-chart-data");
  if (churn) {
    makeChart("churnRiskChart", {
      type: "doughnut",
      data: {
        labels: churn.labels,
        datasets: [{ data: churn.values, backgroundColor: [rust, gold, teal] }],
      },
      options: { responsive: true, plugins: { legend: { position: "bottom" } } },
    });
  }

  const pricing = readJson("pricing-chart-data");
  if (pricing) {
    makeChart("pricingChart", {
      type: "bar",
      data: {
        labels: pricing.labels,
        datasets: [
          { label: "Current price (P)", data: pricing.current, backgroundColor: navy },
          { label: "Proposed price (P)", data: pricing.proposed, backgroundColor: teal },
        ],
      },
      options: { responsive: true },
    });
  }
})();
