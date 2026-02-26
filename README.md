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

The `ticker_data_mag7` table is pre-loaded. Complete **Lab 3** before starting the agent labs (Labs 4–7).

---

## Labs

| Lab | Topic | What You Build |
|-----|-------|---------------|
| [Lab 0 — Setup](labs/00-setup.md) | Environment | Verify workspace access and data |
| [Lab 1 — Genie Space](labs/01-genie-setup.md) | Genie | Natural language SQL over MAG-7 stock price and financial data |
| [Lab 2 — Apps](labs/02-apps.md) | Databricks Apps | Deploy the MAG-7 Ticker Explorer as a Databricks App |
| [Lab 3 — Data Ingestion](labs/03-data-ingestion.md) | ETL | Load financial data into Unity Catalog Delta tables using Databricks Assistant, Data Science Agent, and AI Dev Kit |
| [Lab 4 — Information Extraction](labs/04-information-extraction-agent.md) | AgentBricks | Extract structured financial data from SEC filings |
| [Lab 5 — Custom LLM Agent](labs/05-custom-llm-agent.md) | AgentBricks | Generate financial analysis from earnings call transcripts |
| [Lab 6 — Knowledge Assistant](labs/06-knowledge-assistant.md) | AgentBricks | Multi-document search across all five filing types |
| [Lab 7 — Multi-Agent Supervisor](labs/07-multi-agent.md) | AgentBricks | Orchestrate Genie and Knowledge Assistant to answer complex financial questions |
| [Lab 8 — AI Dev Kit Skills](labs/08-ai-dev-kit-skills.md) | AI Dev Kit | Use skills to accelerate and automate every lab |

---

## Prerequisites

- Databricks workspace with AgentBricks enabled
- Unity Catalog with a catalog and schema you can write to
- For Labs 3 and 8: [AI Dev Kit](https://github.com/databricks-solutions/ai-dev-kit) and [Claude Code](https://github.com/anthropics/claude-code) installed locally
