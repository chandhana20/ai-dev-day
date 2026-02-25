# Lab 1 — Information Extraction Agent (KIE)

**Time:** ~25 minutes
**Goal:** Build an AI agent that automatically extracts structured financial metrics (revenue, net income, debt ratios, etc.) from 10-K SEC filings and stores them in a Delta table.

**Business Problem:** Equity analysts spend hours manually pulling numbers from 10-Ks. This agent does it in seconds — consistently and at scale.

---

## Overview

You will use **AgentBricks → Key Information Extraction (KIE)** to:
1. Define the fields you want to extract (revenue, net income, etc.)
2. Run the agent against sample 10-K documents
3. Tune field definitions to improve accuracy
4. Export results to a Delta table via a pipeline

---

## Step 1 — Create a New KIE Agent

1. Go to **AI & BI → AgentBricks**.
2. Click **Create Agent**.
3. Select **Key Information Extraction**.
4. Give it a name: `nvidia-10k-extractor`
5. Click **Next**.

---

## Step 2 — Connect Your Data Source

1. Under **Data Source**, select **Unity Catalog Volume**.
2. Choose: **main → cp_nvidia → 10k**
3. Click **Sample Documents** — AgentBricks will pull a few PDFs to test against.
4. Click **Next**.

---

## Step 3 — Define the Fields to Extract

You will define the schema — the specific data points you want the agent to pull from each filing.

Click **Add Fields** and add the following one by one:

| Field Name | Type | Description |
|------------|------|-------------|
| `company_name` | string | Legal name of the company on the 10-K cover page |
| `stock_symbol` | string | Stock ticker symbol (e.g., AAPL, NVDA) |
| `fiscal_year_end` | string | End date of the fiscal year in format dd-mm-yyyy |
| `total_revenue` | number | Total company revenue in USD millions |
| `operating_income` | number | Operating income in USD millions |
| `net_income` | number | Net income in USD millions |
| `total_assets` | number | Total assets in USD millions |
| `total_liabilities` | number | Total liabilities in USD millions |
| `long_term_debt` | number | Long-term debt in USD millions |
| `cash_and_cash_equivalents` | number | Cash and equivalents in USD millions |
| `capital_expenditures` | number | Capital expenditure in USD millions |
| `r_and_d_expense` | number | Research and development expense in USD millions |
| `total_employees` | number | Total number of full-time employees |
| `principal_executive_officer` | string | Name of the CEO |
| `independent_auditor` | string | Name of the auditing firm |

> **Tip:** Click **Auto-generate fields** first — AgentBricks may suggest many of these automatically.

---

## Step 4 — Run Against Sample Documents

1. Click **Run on Samples**.
2. Wait ~1–2 minutes while the agent processes the sample 10-K PDFs.
3. Review the results table — each column is a field you defined, each row is a document.

**Check for issues:**
- Are dates formatted correctly? (should be `dd-mm-yyyy`)
- Are numeric fields returning numbers, not strings?
- Are any fields returning `null` when you'd expect a value?

---

## Step 5 — Tune Field Definitions

Fix any issues you spotted. Common tweaks:

**Fix the date format:**
1. Click on the `fiscal_year_end` field.
2. Update the description to:
   > "The end date of the company's fiscal year. Must be in the format dd-mm-yyyy."
3. Click **Save**.

**Fix numeric fields returning as strings:**
1. Click on any numeric field (e.g., `operating_income`) that returned a string.
2. Change the **Type** from `string` to `number`.
3. Update the description to include: "Should be a numerical value in USD millions."
4. Click **Save**.

After making changes, click **Re-run on Samples** to see improvements.

---

## Step 6 — Run Evaluation

1. Click the **Evaluation** tab.
2. Review the assessments — the LLM judge scores each field extraction.
3. Drill into individual results to see which fields scored well vs. poorly.
4. If a field is consistently wrong, go back to Step 5 and refine its description.

---

## Step 7 — (Optional) Optimize for Cost

1. Once you're happy with quality, click **Optimize**.
2. AgentBricks will find a smaller, cheaper model that achieves similar quality.
3. Compare the **quality score** and **cost per document** between models.
4. Select your preferred model.

---

## Step 8 — Create a Pipeline to Populate a Delta Table

1. Click **Use** → **Create ETL Pipeline**.
2. Name the pipeline: `10k-extraction-pipeline`
3. Click **Start** — this will process all 10-K PDFs and write results to a Delta table.
4. Once complete, go to **main → cp_nvidia** in the Catalog and find the new table.
5. Click **Sample Data** to verify the extracted fields look correct.

> The pipeline creates a structured Delta table you can query with SQL or use in Genie (Lab 4).

---

## Verify Your Output

Run this in the SQL Editor to confirm your pipeline worked:

```sql
SELECT company_name, stock_symbol, fiscal_year_end, total_revenue, net_income
FROM main.cp_nvidia.`10k-extraction-pipeline_responses_wide`
ORDER BY company_name;
```

You should see one row per 10-K filing with structured financial data.

---

## Summary

You built an agent that:
- Reads raw PDF filings from a Unity Catalog volume
- Extracts 15+ structured financial fields per document
- Stores results in a queryable Delta table

**Next:** [Lab 2 — Custom LLM Agent for Earnings Call Analysis](02-custom-llm-agent.md)
