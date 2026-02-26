# Lab 2 — Apps: Deploy the MAG-7 Ticker Explorer

**Time:** ~20 minutes
**Goal:** Deploy a Streamlit app as a **Databricks App** that reads live from `ticker_data_mag7` and lets anyone explore MAG-7 stock data through an interactive UI — no Databricks account required to use it.

**Business Problem:** Analysts need a shareable, always-on view of MAG-7 stock data without opening notebooks or writing SQL. A Databricks App bridges the gap between your data platform and business users.

---

## Overview

You will:
1. Review the app code and what it displays
2. Write the app files to your workspace
3. Create and deploy the app using the Databricks CLI
4. Share the URL with your team

The data (`catalog.schema.ticker_data_mag7`) is already loaded from Lab 1.

---

## What the App Shows

| Feature | Description |
|---------|-------------|
| KPI tiles | Latest close price and day delta for each selected ticker |
| Closing price chart | Line chart of price over a selectable date range |
| Trading volume chart | Bar chart of daily volume by ticker |
| Data table | Filterable, sortable table with CSV download |
| Sidebar filters | Ticker selection, date range, and sort order |

---

## Step 1 — Review the App Code

The app is in `apps/mag7-ticker-app/app.py`. Open it to see how it works:

- **Authentication**: Uses `databricks.sdk.core.Config` — picks up credentials automatically inside a Databricks App
- **Data loading**: Connects to your SQL warehouse via `databricks-sql-connector`, caches results for 5 minutes
- **Query**: Reads `price_open`, `price_close`, `volume`, `pe_trailing`, `pe_forward`, `ev_ebitda`, `market_cap`, and `beta` from `ticker_data_mag7`

The app config (`app.yaml`) sets the warehouse ID via environment variable:

```yaml
command: ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]

env:
  - name: DATABRICKS_WAREHOUSE_ID
    value: "your-warehouse-id"
```

---

## Step 2 — Find Your SQL Warehouse ID

1. In Databricks, go to **SQL Warehouses** in the left sidebar.
2. Click your warehouse and copy the ID from the URL or the connection details.
3. It looks like: `75fd8278393d07eb`

---

## Step 3 — Copy the App to Your Workspace

In a Databricks notebook, run:

```python
import subprocess

# Copy app files to your workspace
subprocess.run([
    "databricks", "workspace", "import-dir",
    "apps/mag7-ticker-app",
    f"/Workspace/Users/{current_user}/mag7-ticker-app",
    "--overwrite"
])
```

Or manually upload `apps/mag7-ticker-app/` via the Workspace UI.

---

## Step 4 — Update the Warehouse ID

Update `app.yaml` to use your warehouse ID:

```yaml
env:
  - name: DATABRICKS_WAREHOUSE_ID
    value: "your-warehouse-id-here"
```

Also update the table reference in `app.py` if your catalog/schema differ:

```python
TABLE_NAME = "your_catalog.your_schema.ticker_data_mag7"
```

---

## Step 5 — Deploy the App

Open a terminal and run:

```bash
# Create the app (once per deployment)
databricks apps create mag7-ticker-app

# Deploy your code
databricks apps deploy mag7-ticker-app \
  --source-code-path /Workspace/Users/your-email/mag7-ticker-app
```

The CLI will show a progress bar. When complete, it prints the app URL:

```
https://mag7-ticker-app-<workspace-id>.aws.databricksapps.com
```

---

## Step 6 — Test the App

1. Open the URL in your browser.
2. Use the sidebar to filter tickers and date range.
3. Check that the KPI tiles show current prices.
4. Download a filtered CSV using the button at the bottom of the table.

---

## Step 7 — Share the App

Databricks Apps URLs are shareable with anyone who has Databricks workspace access. To control who can view it:

1. Go to **Apps** in the Databricks sidebar.
2. Find `mag7-ticker-app` → **Permissions**.
3. Add users or groups.

---

## Summary

You deployed a production-ready data app that:
- Reads live from Unity Catalog with 5-minute caching
- Handles authentication automatically via the Databricks Apps runtime
- Requires no infrastructure setup or Kubernetes knowledge

**Next:** [Lab 5 — Custom LLM Agent](05-custom-llm-agent.md)
