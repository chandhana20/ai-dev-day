# Lab 0 — Setup & Environment Check

**Time:** ~10 minutes
**Goal:** Verify you can access the workspace, find the data, and open AgentBricks.

---

## Step 1 — Log into Databricks

1. Open your browser and go to: **https://e2-demo-west.cloud.databricks.com/**
2. Log in with your credentials.

---

## Step 2 — Verify Your Data

1. In the left sidebar, click **Catalog**.
2. Navigate to: **main → cp_nvidia**
3. Confirm you can see the following volumes under the **Volumes** tab:
   - `10k`
   - `10q`
   - `annual_report`
   - `call_transcripts`
   - `earning_releases`
4. Click into the `10k` volume and confirm you can see the PDF files (Apple, Amazon, Google, Meta, MSFT, NVIDIA, Tesla 10-Ks).

> **If any volumes are missing**, let your lab facilitator know before continuing.

---

## Step 3 — Verify the Delta Tables

Still in **main → cp_nvidia**, click the **Tables** tab and confirm these tables exist:

- `10k_parsed`
- `call_transcripts_parsed`
- `ticker_data_mag7`

Click `ticker_data_mag7` → **Sample Data** to make sure it has rows.

> These tables were pre-built for you from the raw PDFs. Lab 1 will show you how to create your own.

---

## Step 4 — Open AgentBricks

1. In the left sidebar, click **AI & BI** → **AgentBricks**.
2. You should see the AgentBricks home page.
3. If you see a "Get Started" or "Create Agent" button, you are ready.

---

## Step 5 — Quick Sanity Check

Run this quick SQL to confirm data is accessible:

1. Go to **SQL Editor** in the left sidebar.
2. Select your SQL warehouse.
3. Run:

```sql
SELECT company_name, price_close, date
FROM main.cp_nvidia.ticker_data_mag7
WHERE company_name = 'NVDA'
ORDER BY date DESC
LIMIT 5;
```

You should see NVIDIA stock price rows.

---

## You're Ready!

Once all steps above pass, move on to **[Lab 1 — Information Extraction Agent](01-information-extraction-agent.md)**.
