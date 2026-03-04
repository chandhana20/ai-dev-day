# Lab 6 — Knowledge Assistant (Multi-Document RAG)

**Time:** ~25 minutes
**Goal:** Build a retrieval-augmented AI assistant that can answer research questions across all financial documents — 10-Ks, 10-Qs, annual reports, earnings releases, and call transcripts — simultaneously.

**Business Problem:** Analysts toggle across dozens of PDFs to answer a single client question. This agent answers in seconds and cites its sources.

---

## Overview

You will use  Knowledge Assistant (KA)** to:
1. Create a multi-source knowledge assistant
2. Connect all five document volumes as separate knowledge bases
3. Configure the agent to know when to use each source
4. Test and refine with guardrail instructions

---

## Step 1 — Create a Knowledge Assistant

1. Go to **AgentBricks**.
2. Click **Create Agent**.
3. Select **Knowledge Assistant**.
4. Name it: `mag7-financial-research-assistant`
5. Click **Next**.

---

## Step 2 — Add Knowledge Sources (Volumes)

You will add each document folder as a separate knowledge source. This lets you give the agent specific instructions on when to use each one.

**Add Knowledge Source 1 — 10-K Filings:**
1. Click **Add Knowledge Source** → **Unity Catalog Volume**.
2. Select: **your catalog → your schema → 10k**
3. Set the name: `10K Filings`
4. Add this description:
   > "Contains annual 10-K SEC filings for the Magnificent 7 companies (Apple, Amazon, Google, Meta, Microsoft, NVIDIA, Tesla) covering the past several years. Use this for annual financial metrics, risk factors, business overviews, and management discussions."
5. Click **Add**.

**Add Knowledge Source 2 — 10-Q Filings:**
1. Click **Add Knowledge Source** → **Unity Catalog Volume**.
2. Select: **your catalog → your schema → 10q**
3. Set the name: `10Q Filings`
4. Description:
   > "Contains quarterly 10-Q SEC filings for the Magnificent 7. Use for quarterly financial results, recent developments, and updated risk disclosures."
5. Click **Add**.

**Add Knowledge Source 3 — Earnings Releases:**
1. Click **Add Knowledge Source** → **Unity Catalog Volume**.
2. Select: **your catalog → your schema → earning_releases**
3. Set the name: `Earnings Releases`
4. Description:
   > "Contains earnings press releases, investor slides, and CFO commentary published by Magnificent 7 companies during quarterly earnings. Use for headline financial results, guidance, and investor-facing summaries."
5. Click **Add**.

**Add Knowledge Source 4 — Call Transcripts:**
1. Click **Add Knowledge Source** → **Unity Catalog Volume**.
2. Select: **your catalog → your schema → call_transcripts**
3. Set the name: `Earnings Call Transcripts`
4. Description:
   > "Contains full earnings call transcripts for the Magnificent 7, including CEO/CFO prepared remarks and analyst Q&A. Use for management commentary, forward guidance tone, and competitive signals."
5. Click **Add**.

**Add Knowledge Source 5 — Annual Reports:**
1. Click **Add Knowledge Source** → **Unity Catalog Volume**.
2. Select: **your catalog → your schema → annual_report**
3. Set the name: `Annual Reports`
4. Description:
   > "Contains full shareholder annual reports for the Magnificent 7. Use for narrative company strategy, letter to shareholders, and long-term outlook."
5. Click **Add**.

---

## Step 3 — Configure Agent Instructions

1. Click the **Instructions** tab.
2. Paste the following:

```
This agent answers financial research questions about the Magnificent 7 technology companies only. The companies and their tickers are:
- Alphabet (Google): GOOGL / GOOG
- Amazon: AMZN
- Apple: AAPL
- Meta Platforms: META
- Microsoft: MSFT
- NVIDIA: NVDA
- Tesla: TSLA

Only use information from the provided knowledge sources. Do not use general knowledge or make up financial data. If the answer is not found in the documents, say so clearly.

Always cite the source document and relevant section in your response.
```

3. Click **Save**.

---

## Step 4 — Sync and Build

1. Click **Sync and Build**.
2. This ingests all PDFs, chunks the text, creates embeddings, and builds the vector index.
3. **This takes 15–30 minutes** depending on document count. You can continue to the next step while it runs, or take a break.

> A progress bar will show the sync status. The UI will update with links to the deployed agent once complete.

---

## Step 5 — Test Your Agent

Once syncing is complete:

1. Click **Test in AI Playground**.
2. Try these sample questions:

**Basic retrieval:**
> "What were Apple's total revenues in their most recent 10-K?"

**Multi-document:**
> "Compare NVIDIA and Microsoft's R&D expenses from their latest annual filings."

**Risk-focused:**
> "What are the top 3 risks disclosed by Amazon in its most recent 10-K?"

**Earnings call:**
> "What did NVIDIA management say about data center demand on their most recent earnings call?"

**Cross-source:**
> "Summarize NVIDIA's guidance from the last earnings call and compare it to what they reported in the 10-Q."

For each answer, check:
- Is the response accurate?
- Does it cite a source document?
- Is it staying within the Mag 7 scope?

---

## Step 6 — Improve Quality with Instructions

**Test a guardrail:**

Try asking:
> "What is IBM's current stock price?"

The agent may try to answer using its pre-trained knowledge. To prevent this:

1. Go to **Instructions** (already set in Step 3).
2. Confirm the instruction explicitly restricts to Mag 7 only.
3. Click **Update Agent**.
4. Try the IBM question again — it should now decline or redirect.

---

## Step 7 — (Optional) Feedback & Labeling

For production use, you can improve the agent with human feedback:

1. Click the **Improve Quality** tab.
2. Add 5–10 test questions relevant to your use case.
3. Click **Start Labeling Session** — reviewers can rate answers as good/bad and provide corrections.
4. Once you have 20+ labeled examples, Databricks automatically refines the agent.

> This is how you tune the agent for your firm's specific terminology and priorities.

---

## Summary

You built a knowledge assistant that:
- Searches across 5 separate document collections simultaneously
- Answers natural language research questions with source citations
- Is guardrailed to stay within the Mag 7 universe

**Next:** [Lab 7 — Multi-Agent Orchestration](07-multi-agent.md)
