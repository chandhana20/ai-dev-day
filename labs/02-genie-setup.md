# Lab 1 — Genie Space (Natural Language SQL)

**Time:** ~20 minutes
**Goal:** Build a Genie Space that lets anyone ask quantitative financial questions in plain English — combining live stock ticker data with the structured metrics you extracted in Lab 1.

**Business Problem:** Traders and analysts need to quickly slice and query structured financial data without writing SQL. Genie makes this conversational.

---

## Overview

You will use **Databricks Genie** to:
1. Create a Genie room connected to two Delta tables
2. Teach Genie how to join them with a sample query
3. Test natural language queries
4. (Optional) Add curated questions and instructions

---

## Step 1 — Navigate to Genie

1. In the left sidebar, click → Genie**.
2. Click **Create Genie Space**.
3. Name it: `mag7-financial-analytics`
4. Click **Create**.

---

## Step 2 — Add Your Tables

Add both of the following tables to this Genie space:

**Table 1 — Stock Ticker Data:**
1. Click **Add Table**.
2. Select: catalog.schema.ticker_data_mag7
3. This table contains daily stock prices (open, close, volume, date) for the Mag 7.
4. Click **Add**.

**Table 2 — Extracted 10-K Financial Data:**
1. Click **Add Table**.
2. Select: [your KIE pipeline table from Lab 1]**
   - This is the wide table created by the extraction pipeline (e.g., `10k-extraction-pipeline_responses_wide`)
3. Click **Add**.

---

## Step 3 — Teach Genie How to Join the Tables

The two tables use different identifiers — `catalog.schema.ticker_data_mag7` uses `company_name` (e.g., `MSFT`) while the KIE table uses `stock_symbol`. You need to tell Genie the right way to join them.

1. In the Genie , add SQL query as instruction:
To calculate max close price 
```sql
SELECT
  MAX(t.price_close)    AS max_close_price
FROM main.fins_agent_bricks_demo.ticker_data_mag7 t
JOIN main.fins_agent_bricks_demo.`kie-87141233-endpoint_responses_wide` k
  ON t.company_name = k.stock_symbol
WHERE t.company_name = 'AAPL'
  AND t.price_close IS NOT NULL;
```

2. Run it and confirm it returns results.
3. Click **Add as Instruction** — this teaches Genie the correct join pattern for all future queries.

> This is how Genie learns. Any query you mark as an instruction becomes part of its reasoning context.

---

## Step 4 — Add Table Descriptions

Help Genie understand what each table contains:

1. Click on **catalog.schema.ticker_data_mag7** in the tables panel.
2. Add description:
   > "Daily stock market data for the Magnificent 7 companies. Contains company_name (ticker symbol like AAPL, NVDA), date, price_open, price_close, and trading volume. Use for stock performance, price trends, and trading analysis."
3. Save.

4. Click on your KIE table.
5. Add description:
   > "Structured financial data extracted from 10-K annual SEC filings. Contains one row per filing with fields like total_revenue, net_income, long_term_debt, r_and_d_expense, and total_employees. Join to ticker data on stock_symbol = company_name."
6. Save.

---

## Step 5 — Test Natural Language Queries

Try asking Genie these questions:

**Stock performance:**
> "What was NVIDIA's highest stock price?"
> "What was Microsoft's max stock price"
> I'm building a portfolio. Which MAG7 stock had the most consistent growth and what was its best month?
>  Which MAG7 stock had the highest average closing price in 2025?

For each answer, check that Genie:
- Returns a SQL query it used (visible in the response)
- Shows a table or chart
- Used the correct join when both tables were needed



## Step 7 — (Optional) Add Genie Instructions

You can add free-text instructions to guide Genie's behavior:

1. Click **Instructions**.
2. Add:

```
This Genie space focuses on the Magnificent 7 companies: Apple (AAPL), Amazon (AMZN),
Google/Alphabet (GOOG/GOOGL), Meta (META), Microsoft (MSFT), NVIDIA (NVDA), Tesla (TSLA).

Financial figures from the KIE table are in USD millions.
Always clarify units in your responses.
```

3. Click **Save**.

---

## Summary

You built a Genie space that:
- Connects live stock data with extracted 10-K fundamentals
- Answers plain English financial questions with SQL
- Knows how to correctly join both data sources

**Next:** [Lab 3 — Data Ingestion](03-data-ingestion.md)
