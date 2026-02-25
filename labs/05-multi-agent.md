# Lab 5 — Multi-Agent Orchestration (Client Advisory Copilot)

**Time:** ~20 minutes
**Goal:** Wire together your Genie space (quantitative analysis) and Knowledge Assistant (qualitative analysis) into a single supervisor agent — an AI copilot that answers complex financial questions requiring both structured data and document research.

**Business Problem:** A relationship manager asks: *"Should I be concerned about Microsoft's debt levels given their recent earnings call guidance?"* — answering this requires SQL queries AND document retrieval. One agent can't do both alone.

---

## Overview

You will use **AgentBricks → Multi-Agent Supervisor (MAS)** to:
1. Create a supervisor agent that routes questions to the right tool
2. Connect your Genie space and Knowledge Assistant as tools
3. Test queries that require both tools working together

---

## Architecture

```
User Question
      │
      ▼
 Supervisor Agent
   /          \
Genie          Knowledge Assistant
(quantitative) (qualitative)
Stock prices   10-K / 10-Q
KIE financials Earnings transcripts
               Annual reports
```

The supervisor decides which tool to call — or calls both — depending on the question.

---

## Prerequisites

Before starting this lab, confirm you have:
- ✅ Lab 1 complete: KIE pipeline table exists in `main.cp_nvidia`
- ✅ Lab 3 complete: Knowledge assistant `mag7-financial-research-assistant` is deployed
- ✅ Lab 4 complete: Genie space `mag7-financial-analytics` is active

---

## Step 1 — Create a Multi-Agent Supervisor

1. Go to **AI & BI → AgentBricks**.
2. Click **Create Agent**.
3. Select **Multi-Agent Supervisor**.
4. Name it: `mag7-client-advisory-copilot`
5. Click **Next**.

---

## Step 2 — Add the Genie Space as a Tool

1. Click **Add Tool**.
2. Select **Genie Space**.
3. Choose: `mag7-financial-analytics` (created in Lab 4).
4. Set the tool name: `Financial Data Analyst`
5. Add this description:
   > "Use this tool for quantitative questions that require SQL queries. Handles stock price data, trading volumes, and structured financial metrics extracted from 10-K filings (revenue, net income, debt, R&D spend, etc.). Good for comparisons, rankings, and numerical lookups."
6. Click **Add**.

---

## Step 3 — Add the Knowledge Assistant as a Tool

1. Click **Add Tool**.
2. Select **Knowledge Assistant**.
3. Choose: `mag7-financial-research-assistant` (created in Lab 3).
4. Set the tool name: `Financial Research Analyst`
5. Add this description:
   > "Use this tool for qualitative questions that require searching financial documents. Handles 10-K/10-Q filings, earnings call transcripts, annual reports, and earnings releases. Good for risk factors, management commentary, guidance tone, and narrative analysis."
6. Click **Add**.

---

## Step 4 — Configure the Supervisor Agent Description

In the **Agent Description** field, add:

```
This agent answers financial research questions about the Magnificent 7 technology companies
(Apple, Amazon, Google/Alphabet, Meta, Microsoft, NVIDIA, Tesla).

It has access to two tools:
1. Financial Data Analyst — for quantitative questions (stock prices, financial metrics, comparisons)
2. Financial Research Analyst — for qualitative questions (filings, transcripts, management commentary)

For complex questions, call both tools and synthesize their answers into a single coherent response.
Always specify which sources were used in your response.
```

Click **Save**.

---

## Step 5 — Test the Supervisor Agent

Try these questions, which are designed to require both tools:

---

**Question 1 — Quantitative only (Genie):**
> "What was NVIDIA's highest stock price in the past 12 months?"

*Expected behavior:* Supervisor calls the Genie tool only. Returns a number with a date.

---

**Question 2 — Qualitative only (Knowledge Assistant):**
> "What risks did Apple disclose in their most recent 10-K regarding supply chain?"

*Expected behavior:* Supervisor calls the Knowledge Assistant only. Returns bullet points with citations.

---

**Question 3 — Both tools required:**
> "What was Microsoft's max stock price, and has their recent earnings guidance justified that valuation?"

*Expected behavior:* Supervisor calls **both** tools — Genie for the price, Knowledge Assistant for the guidance commentary. Returns a synthesized answer combining both.

---

**Question 4 — Strategic advisory:**
> "I hold a large position in NVIDIA. Based on their recent earnings call and financial metrics, should I be concerned about near-term risks?"

*Expected behavior:* Both tools called. Response covers stock trends from Genie + risk/guidance signals from transcripts and filings.

---

**Question 5 — Comparison:**
> "Compare NVIDIA and Microsoft: who has stronger revenue growth, and what are each company's top strategic priorities according to management?"

*Expected behavior:* Genie for revenue numbers, Knowledge Assistant for strategic priorities from annual reports/transcripts.

---

## Step 6 — Review the Reasoning Trace

For each query, click **Show Trace** to inspect:
- Which tool was called first
- What was passed to each tool
- How the supervisor combined the results

This is useful for debugging — if the agent gives a wrong answer, the trace shows you exactly why.

---

## Step 7 — (Optional) Tune the Routing Logic

If the supervisor is routing to the wrong tool:

1. Click **Instructions**.
2. Add explicit routing guidance, for example:
   > "Always use the Financial Data Analyst for any question involving specific numbers, prices, percentages, or date ranges. Always use the Financial Research Analyst for questions involving 'what did management say', 'what are the risks', or 'summarize the [document]'."
3. Click **Update Agent** and re-test.

---

## Congratulations — Build-a-Thon Complete!

You have built a full AI-powered financial intelligence platform:

| Agent | Purpose |
|-------|---------|
| **KIE Agent** | Extracts structured data from 10-K PDFs into Delta tables |
| **Custom LLM Agent** | Generates analyst memos from earnings call transcripts |
| **Knowledge Assistant** | Answers research questions across all filings with citations |
| **Genie Space** | Natural language SQL over stock + financial data |
| **Multi-Agent Supervisor** | Single copilot that routes and synthesizes across all agents |

---

## What's Next?

- **Connect to your firm's real data** — swap the Mag 7 PDFs for your actual client filings
- **Add more document types** — research reports, broker notes, regulatory filings
- **Deploy to users** — each agent has a shareable URL and can be embedded in apps
- **Set up automated pipelines** — refresh data as new 10-Ks and transcripts are published
- **Explore the Databricks notebook** in `notebooks/01_data_ingestion.py` to understand how the raw PDFs were processed into Delta tables
