# AI Dev Day — Finance Build-a-Thon

**Welcome to the NVIDIA AI Dev Day Build-a-Thon!**

In this hands-on lab you will build a complete AI-powered financial analysis platform on Databricks using **AgentBricks** and **Genie**. No coding required for most steps — just follow the labs in order.

---

## What You'll Build

You are building tools for **Everest Capital**, a mid-sized investment bank whose analysts spend hours manually reading SEC filings, earnings calls, and press releases. By the end of this build-a-thon, you will have:

| Lab | What You Build | Purpose |
|-----|---------------|---------|
| [Lab 0 — Setup](labs/00-setup.md) | Workspace & data access | Verify your environment |
| [Lab 1 — Information Extraction Agent](labs/01-information-extraction-agent.md) | KIE Agent on 10-K filings | Auto-extract financial metrics from PDFs into Delta tables |
| [Lab 2 — Custom LLM Agent](labs/02-custom-llm-agent.md) | Analyst Memo Generator | Turn earnings call transcripts into executive memos |
| [Lab 3 — Knowledge Assistant](labs/03-knowledge-assistant.md) | Multi-doc RAG Agent | Answer research questions across all filings |
| [Lab 4 — Genie Space](labs/04-genie-setup.md) | Natural Language SQL | Query stock + financial data conversationally |
| [Lab 5 — Multi-Agent Orchestration](labs/05-multi-agent.md) | Supervisor Agent | Wire everything into a single client advisory copilot |

---

## The Data

All datasets are pre-loaded in your workspace under `/Volumes/main/cp_nvidia/`.

| Folder | Contents |
|--------|----------|
| `10k/` | 10-K annual filings — Apple, Amazon, Google, Meta, Microsoft, NVIDIA, Tesla |
| `10q/` | 10-Q quarterly filings |
| `annual_report/` | Full annual reports |
| `call_transcripts/` | Earnings call transcripts |
| `earning_releases/` | Earnings press releases and slide decks |

**Delta tables** (pre-built for you):
- `main.cp_nvidia.10k_parsed` — extracted text from 10-K PDFs
- `main.cp_nvidia.call_transcripts_parsed` — extracted text from call transcripts
- `main.cp_nvidia.ticker_data_mag7` — daily stock price data for the Magnificent 7

---

## Prerequisites

- Access to `https://e2-demo-west.cloud.databricks.com/`
- Your workspace: `main.cp_nvidia` schema
- AgentBricks enabled (confirm with your lab facilitator)

---

## Lab Order

Follow the labs sequentially. Each lab builds on the previous one.

```
Lab 0 → Lab 1 → Lab 2 → Lab 3 → Lab 4 → Lab 5
Setup    KIE     CLLM     KA     Genie    MAS
```

**Time estimate per lab:** ~20–30 minutes each

---

## Support

If you get stuck, ask your lab facilitator or refer to the [Databricks AgentBricks docs](https://docs.databricks.com/en/generative-ai/agent-bricks/index.html).
