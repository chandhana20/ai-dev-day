# AI Dev Day

**Welcome to the AI Dev Day!**

In this hands-on lab you will build a complete AI-powered financial analysis platform on Databricks using **AgentBricks**, **Genie** & all the other ai tools. Just follow the labs in order.

---

## What You'll Build

You are building tools for **Everest Capital**, a mid-sized investment bank whose analysts spend hours manually reading SEC filings, earnings calls, and press releases. By the end of this build-a-thon, you will have:

| Lab | What You Build | Purpose |
|-----|---------------|---------|
| [Lab 0 — Setup](labs/00-setup.md) | Workspace & data access | Verify your environment |
| [Lab 0b — Data Ingestion](labs/00b-data-ingestion.md) | ETL pipeline (PDFs → Delta tables) | Build with Databricks Assistant, Data Science Agent & AI Dev Kit |
| [Lab 1 — Information Extraction Agent](labs/01-information-extraction-agent.md) | KIE Agent on 10-K filings | Auto-extract financial metrics from PDFs into Delta tables |
| [Lab 2 — Custom LLM Agent](labs/02-custom-llm-agent.md) | Analyst Memo Generator | Turn earnings call transcripts into executive memos |
| [Lab 3 — Knowledge Assistant](labs/03-knowledge-assistant.md) | Multi-doc RAG Agent | Answer research questions across all filings |
| [Lab 4 — Genie Space](labs/04-genie-setup.md) | Natural Language SQL | Query stock + financial data conversationally |
| [Lab 5 — Multi-Agent Orchestration](labs/05-multi-agent.md) | Supervisor Agent | Wire everything into a single client advisory copilot |
| [Lab 6 — AI Dev Kit Skills](labs/06-ai-dev-kit-skills.md) | Skills-accelerated workflow | Use skills to automate and enrich every lab |

---

## The Data

All datasets are pre-loaded in your workspace under `/Volumes/catalog/schema/`.

| Folder | Contents |
|--------|----------|
| `10k/` | 10-K annual filings — Apple, Amazon, Google, Meta, Microsoft, NVIDIA, Tesla |
| `10q/` | 10-Q quarterly filings |
| `annual_report/` | Full annual reports |
| `call_transcripts/` | Earnings call transcripts |
| `earning_releases/` | Earnings press releases and slide decks |

---

## Prerequisites

- Access to your Databricks workspace
- Your workspace schema: `catalog.schema`
- AgentBricks enabled (confirm with your lab facilitator)
- **For Lab 0b & Lab 6:** [AI Dev Kit](https://github.com/databricks-solutions/ai-dev-kit) installed locally and Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)

---

## Lab Order

Follow the labs sequentially. Each lab builds on the previous one.

```
Lab 0 → Lab 0b → Lab 1 → Lab 2 → Lab 3 → Lab 4 → Lab 5 → Lab 6
Setup   Ingest    KIE     CLLM     KA     Genie    MAS    Skills
```

**Time estimate per lab:** ~20–30 minutes each

> **Lab 0b** is where the raw PDFs become queryable Delta tables. All agent labs depend on it.
> **Lab 6** can be done alongside any other lab — use it to accelerate whatever you're building.

---

## Support

If you get stuck, ask your lab facilitator or refer to the [Databricks AgentBricks docs](https://docs.databricks.com/en/generative-ai/agent-bricks/index.html).
