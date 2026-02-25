# Lab 2 — Custom LLM Agent (Earnings Call Analyst Memo)

**Time:** ~25 minutes
**Goal:** Build an AI agent that reads earnings call transcripts and automatically generates structured analyst memos — including an executive summary, financial scorecard, and red/green flags.

**Business Problem:** Traders and portfolio managers need instant signal from earnings calls. Manually reading transcripts delays decisions and creates missed opportunities.

---

## Overview

You will use **AgentBricks → Custom LLM** to:
1. Write a structured prompt that acts like a lead equity research analyst
2. Add quality guidelines to enforce consistent output format
3. Test the agent on real earnings call transcripts
4. Review quality scores and refine

---

## Step 1 — Create a New Custom LLM Agent

1. Go to **AI & BI → AgentBricks**.
2. Click **Create Agent**.
3. Select **Custom LLM**.
4. Name it: `earnings-call-analyst`
5. Click **Next**.

---

## Step 2 — Connect Your Data Source

1. Under **Data Source**, select **Unity Catalog Table**.
2. Choose: **main → cp_nvidia → call_transcripts_parsed**
3. Click **Sample Documents** to load a few transcripts for testing.
4. Click **Next**.

---

## Step 3 — Write the Agent Prompt

In the **Prompt** box, paste the following exactly:

---

```
Role: You are a lead Equity Research Analyst for a well-respected investment firm. You have been given the task of parsing through earnings call transcripts for Magnificent 7 accounts (Apple, Amazon, Google, Meta, Microsoft, NVIDIA, Tesla) in order to generate internal memos for clients and traders.

Analyze ONLY the provided transcript. If a data point is not present, return null — do not guess or infer.

Be specific. Quantify everything. Cite with transcript timestamps (e.g., [CEO, 00:12:34]). Use USD millions unless stated. Include both YoY and QoQ deltas where applicable.

Generate an Analyst Memo (≤ 800 words) using this exact structure:

---

## 1) Executive Summary (≤ 120 words)
- Decision: Increase / Hold / Decrease (pick one) + 3–5 line rationale
- Near-term catalysts (1–2 quarters): product launches, pricing, AI rollouts, regulatory
- Confidence level (0–100%) and top 2 risks that would change the view

## 2) Scorecard vs. Consensus
| Metric | Reported | Consensus | Beat/Miss | YoY % | QoQ % |
|--------|----------|-----------|-----------|-------|-------|
| Revenue | | | | | |
| EPS (diluted) | | | | | |
| Gross Margin | | | | | |
| Operating Margin | | | | | |
| Free Cash Flow | | | | | |
| Guidance (Rev/EPS) | | | | | |

Note: If consensus is not provided, mark as NA.

## 3) KPI & Segment Trends
- List each business segment with growth rates, mix shifts, and pricing/volume/FX effects
- Include unit economics where relevant: ARPU, utilization, bookings/backlog, inventory days

## 4) Management Commentary & Q&A Themes
- Growth drivers (cite timestamps)
- Headwinds: demand, competition, pricing, supply chain, regulation (cite timestamps)
- Cost & Capex trajectory: opex direction, data center / AI capex plans (cite timestamps)
- Capital allocation: buybacks, dividends, net cash/debt changes (cite timestamps)

## 5) Guidance Parse & Implied Math
- Convert all guidance ranges to midpoints
- Compute implied YoY/QoQ change and margin effects
- Note any delta vs. prior guidance and vs. consensus

## 6) Red / Green Flags
🟢 Green (positive signals):
- e.g., improving FCF conversion, durable backlog, pricing power

🔴 Red (risk signals):
- e.g., declining incremental margins, rising DSO, inventory build, guidance cut
```

---

Click **Save Prompt**.

---

## Step 4 — Run on Sample Documents

1. Click **Run on Samples**.
2. Wait ~2 minutes for the agent to process transcript samples.
3. Review the output — each result should follow the 6-section memo structure.

**Check for:**
- Is the scorecard table formatted correctly?
- Are timestamps cited in the commentary?
- Are Red/Green flags in bullet form?
- Is the executive summary under 120 words?

---

## Step 5 — Add Quality Guidelines

Guidelines are field-level rules that help the LLM judge evaluate your agent's output. Add the following:

1. Click the **Guidelines** tab.
2. Click **Add Guideline** (or use **AI-suggest guidelines** and accept the relevant ones).
3. Add each of the following:

| Guideline |
|-----------|
| All quantitative data must be cited with transcript timestamps in format [Role, HH:MM:SS] |
| Financial figures must be in USD millions unless explicitly stated otherwise |
| Executive Summary must be 120 words or fewer |
| Scorecard must be a markdown table; mark consensus as 'NA' if missing |
| Red/Green Flags must use bullet points with supporting transcript evidence |
| Guidance Parse must convert ranges to midpoints and show implied YoY/QoQ deltas |
| All analysis must be strictly based on the provided transcript — return null for missing data, do not guess |
| Memo must use clear markdown section headers matching the specified structure |

4. Click **Save Guidelines**.
5. Click **Re-run on Samples** to see the improvement.

---

## Step 6 — Review Quality Scores

1. Click the **Quality** tab.
2. Inspect the **LLM judge scores** for each output.
3. Click into individual results to see:
   - Which guidelines were followed ✅
   - Which were missed ❌
   - The judge's reasoning
4. If a section consistently fails, go back and refine that guideline's wording.

---

## Step 7 — (Optional) Optimize for Cost

1. Click **Optimize**.
2. Compare the quality-vs-cost tradeoff across model options.
3. Note: Optimization requires ~100 examples. If you have fewer, this option will be grayed out — this is expected.

---

## Test a Sample Query

Once your agent is deployed, open it and try this prompt:

> "Summarize the most recent NVIDIA earnings call. What guidance did management give on data center revenue?"

The agent should return a structured memo with citations from the transcript.

---

## Summary

You built an agent that:
- Reads raw earnings call transcripts
- Generates a structured, citation-backed analyst memo in seconds
- Follows consistent format guidelines enforced by an LLM judge

**Next:** [Lab 3 — Knowledge Assistant](03-knowledge-assistant.md)
