# AI Dev Day — Finance Build-a-Thon

Build a complete AI-powered financial analysis platform on Databricks using AgentBricks, Genie, Spark Declarative Pipelines, Databricks Assistant, Data Science Agent, and Cursor/Claude Code. Each lab is self-contained with step-by-step instructions.

---

## Data

All datasets cover the **Magnificent 7** companies: Apple, Amazon, Alphabet, Meta, Microsoft, NVIDIA, and Tesla.

| Folder | Contents |
|--------|----------|
| `data/10K/` | Annual 10-K SEC filings |
| `data/10Q/` | Quarterly 10-Q SEC filings |
| `data/Annual Report/` | Full shareholder annual reports |
| `data/Call Transcripts/` | Earnings call transcripts |
| `data/Earning Releases/` | Earnings press releases and investor slide decks |
| `data/ticker_data_for_genie.py` | Notebook to load historical stock price data into `catalog.schema.ticker_data_mag7` |

Run `data/ticker_data_for_genie.py` and complete **Lab 0b** before starting the agent labs.

---

## Labs

| Lab | Topic | What You Build |
|-----|-------|---------------|
| [Lab 0 — Setup](labs/00-setup.md) | Environment | Verify workspace access and data |
| [Lab 0b — Data Ingestion](labs/00b-data-ingestion.md) | ETL | PDFs → Delta tables using Databricks Assistant, Data Science Agent, and AI Dev Kit |
| [Lab 1 — Information Extraction](labs/01-information-extraction-agent.md) | AgentBricks KIE | Extract structured financial metrics from 10-K PDFs into Delta tables |
| [Lab 2 — Custom LLM Agent](labs/02-custom-llm-agent.md) | AgentBricks CLLM | Generate analyst memos from earnings call transcripts |
| [Lab 3 — Knowledge Assistant](labs/03-knowledge-assistant.md) | AgentBricks KA | Multi-document RAG over all five filing types |
| [Lab 4 — Genie Space](labs/04-genie-setup.md) | Genie | Natural language SQL over stock price and financial data |
| [Lab 5 — Multi-Agent Supervisor](labs/05-multi-agent.md) | AgentBricks MAS | Orchestrate Genie + Knowledge Assistant into a single advisory copilot |
| [Lab 6 — AI Dev Kit Skills](labs/06-ai-dev-kit-skills.md) | AI Dev Kit | Use skills to accelerate and automate every lab |

---

## Prerequisites

- Databricks workspace with AgentBricks enabled
- Unity Catalog with a catalog and schema you can write to
- For Labs 0b and 6: [AI Dev Kit](https://github.com/databricks-solutions/ai-dev-kit) and [Claude Code](https://github.com/anthropics/claude-code) installed locally
