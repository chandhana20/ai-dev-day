# BONUS Lab 6 — AI Dev Kit Skills: Accelerate Every Step

**Time:** ~20 minutes
**Goal:** Learn how to use the AI Dev Kit's **skills** system to make your AI coding assistant an expert Databricks developer — so you can build, extend, and debug the entire finance platform faster.

---

## What Are Skills?

A **skill** is a markdown file that teaches your AI assistant (Claude Code, Cursor, Windsurf, etc.) Databricks-specific patterns, best practices, and code templates.

Without skills, your AI assistant writes generic Python. With skills, it writes production-ready Databricks code using the right APIs, the right architecture, and the right patterns.

```
Without skills:                     With skills:
──────────────────────────────────────────────────────
"create a pipeline"    →    spark.read.csv(...)
                                ↓
"create a pipeline"    →    @dp.table(name="bronze_events")
+ spark-declarative          def bronze_events():
  -pipelines skill                return spark.readStream
                                      .format("cloudFiles")
                                      .load("/Volumes/...")
```

---

## The Skills Available

The AI Dev Kit ships with 15 skills covering the full Databricks stack:

### For This Build-a-Thon

| Skill | What It Teaches | Use When |
|-------|----------------|----------|
| `spark-declarative-pipelines` | Bronze/silver/gold ETL, Auto Loader, streaming | Building data pipelines (Lab 0b) |
| `agent-bricks` | KA, Genie, MAS creation patterns | Labs 1–5 |
| `databricks-genie` | Genie Space curation, instructions, sample queries | Lab 4 |
| `unstructured-pdf-generation` | Generating test PDFs for RAG | Prototyping new document types |
| `mlflow-evaluation` | Evaluating agent output quality | After Labs 1–3 |
| `model-serving` | Deploying agents to endpoints | Productionizing agents |
| `databricks-unity-catalog` | System tables, lineage, audit | Governance and monitoring |
| `aibi-dashboards` | Creating AI/BI dashboards | Building exec-facing views |
| `databricks-jobs` | Scheduling and orchestrating workflows | Automating the full pipeline |

---

## Step 1 — Install All Skills

In your terminal (from the ai-dev-kit directory):

```bash
cd ai-dev-kit
./databricks-skills/install_skills.sh
```

This creates `.claude/skills/` with all 15 skills and Claude Code loads them automatically.

**To install a single skill manually:**
```bash
mkdir -p .claude/skills
cp -r ai-dev-kit/databricks-skills/agent-bricks .claude/skills/
```

---

## Step 2 — Verify Skills Are Loaded

Open Claude Code and type:

```
What Databricks skills do you have loaded?
```

Claude Code should list the available skills and describe what each one does.

---

## Step 3 — Using Skills to Accelerate Each Lab

### Skill in Action: Agent Bricks (Labs 1–5)

Instead of clicking through the UI manually, you can use the `agent-bricks` skill + MCP tools to automate agent creation:

**Prompt:**
```
Using the agent-bricks skill, create a Knowledge Assistant called
"mag7-10k-research" that answers questions about the 10-K filings
stored in /Volumes/main/fins_agent_bricks_demo/magnificent_seven_unstructured_data/10k/.

Set instructions to: "Only answer questions about Apple, Amazon,
Google, Meta, Microsoft, NVIDIA, and Tesla annual filings."
```

Claude Code will call `create_or_update_ka` with the right parameters and return the tile ID.

---

### Skill in Action: Genie Space (Lab 4)

**Prompt:**
```
Using the databricks-genie skill, create a Genie Space called
"mag7-financial-analytics" with these two tables:
- main.fins_agent_bricks_demo.ticker_data_mag7

Add these sample questions:
- "What was NVIDIA's highest stock price in 2024?"
```

---

### Skill in Action: Multi-Agent Supervisor (Lab 5)

**Prompt:**
```
Using the agent-bricks skill, create a Multi-Agent Supervisor called
"mag7-client-advisory-copilot" with:

Agent 1 - Financial Data Analyst:
  genie_space_id: 01f112c34d0e1e73ae031cc552eb2a88
  description: "Use for quantitative questions: stock prices,
  financial metrics, comparisons, numerical lookups"

Agent 2 - Financial Research Analyst:
  ka_tile_id: 23b6c7e1-b68b-49ae-a397-2b98c5989a5d 
  description: "Use for qualitative questions: management commentary,
  risk factors, earnings call summaries, strategic priorities"

Add instructions: "For complex questions requiring both quantitative
and qualitative analysis, call both tools and synthesize the results."
```

---

### Skill in Action: MLflow Evaluation (Post-Labs)

Once your agents are built, use the evaluation skill to measure quality:

**Prompt:**
```
Using the mlflow-evaluation skill, create an evaluation script that:
- Tests the mag7-client-advisory-copilot against 10 questions
- Uses the built-in "groundedness" and "answer_correctness" scorers
- Logs results to an MLflow experiment called "finance-copilot-eval"
- Generates a summary report showing pass/fail per question
```

---

### Skill in Action: AI/BI Dashboard

Turn your extracted data into an executive dashboard:

**Prompt:**
```
Using the aibi-dashboards skill, create an AI/BI dashboard called
"Mag7 Financial Overview" with:
- A bar chart of total_revenue by company (from the KIE responses table)
- A line chart of NVDA stock price over time (from catalog.schema.ticker_data_mag7)
- A KPI tile showing average net income across all Mag7 companies
- A table showing each company's long_term_debt vs cash_and_cash_equivalents

Use your catalog.schema as the catalog/schema. Test all SQL before deploying.
```

---

### Skill in Action: Databricks Jobs (Automation)

Schedule the full workflow end-to-end:

**Prompt:**
```
Using the databricks-jobs skill, create a daily job called
"finance-data-refresh" that:
1. Runs the finance-etl-pipeline (SDP pipeline from Lab 0b)
2. After it completes, triggers the KIE extraction pipeline
3. Sends a Slack notification to #finance-ai-team when done
4. Runs daily at 6am UTC, Monday through Friday

Use your catalog.schema for all table targets.
```

---

## Step 4 — Create a Custom Skill for Your Firm

Skills are just markdown files — you can write one for your firm's specific patterns, data models, or naming conventions.

### Create a custom skill:

```bash
mkdir -p .claude/skills/finance-patterns
```

Create `.claude/skills/finance-patterns/SKILL.md`:

```markdown
---
name: finance-patterns
description: "Patterns and conventions for the Finance AI Build-a-Thon.
Use when working with Mag7 financial data, our volume structure, or naming conventions."
---

# Finance AI Build-a-Thon Patterns

## Our Data Locations

| Data Type | Volume Path | Parsed Table |
|-----------|-------------|--------------|
| 10-K filings | /Volumes/catalog/schema/10k/ | catalog.schema.10k_parsed |
| 10-Q filings | /Volumes/catalog/schema/10q/ | catalog.schema.10q_parsed |
| Call transcripts | /Volumes/catalog/schema/call_transcripts/ | catalog.schema.call_transcripts_parsed |
| Earning releases | /Volumes/catalog/schema/earning_releases/ | catalog.schema.earning_releases_parsed |
| Annual reports | /Volumes/catalog/schema/annual_report/ | catalog.schema.annual_reports_parsed |
| Ticker data | N/A | catalog.schema.ticker_data_mag7 |

## Our Companies

The Magnificent 7: AAPL, AMZN, GOOG/GOOGL, META, MSFT, NVDA, TSLA

## Naming Conventions

- Agents: `mag7-[purpose]-agent` (e.g., `mag7-10k-extractor`)
- Pipelines: `mag7-[layer]-[source]` (e.g., `mag7-silver-10k-parsed`)
- Tables: `[doc_type]_parsed` for extracted text, `[doc_type]_wide` for structured KIE output

## Join Pattern for Ticker + KIE Data

Always join on: catalog.schema.ticker_data_mag7.company_name = kie_table.stock_symbol

## Standard Delta Table Options

Always add:
- CLUSTER BY (company_ticker, ingested_at)  -- for performance
- TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')  -- for downstream streaming
```

Now any prompt that references "our data" or "our naming conventions" will automatically follow your firm's standards.

---

## Step 5 — Skill + MCP = Full Automation

The real power is combining skills (knowledge) with MCP tools (actions):

```
Skill          →  Teaches Claude HOW to build on Databricks
MCP Tools      →  Let Claude actually DO it (create, deploy, run)
Your Prompt    →  Tells Claude WHAT to build

Together:      →  Describe it once, get working Databricks infrastructure
```

**Example — full end-to-end in one prompt:**

```
Using the spark-declarative-pipelines, agent-bricks, and
databricks-genie skills:

Build the complete Finance AI platform:
1. Create a Spark Declarative Pipeline to parse earning releases
   from /Volumes/catalog/schema/earning_releases/ into
   catalog.schema.silver_earning_releases
2. Create a Knowledge Assistant over the earning releases volume
3. Create a Genie Space with catalog.schema.ticker_data_mag7 and the silver table
4. Create a Multi-Agent Supervisor combining both
5. Schedule the SDP pipeline to run nightly

Use your catalog and schema.
```

---

## Summary

The AI Dev Kit skills system lets you:

| Action | Without Skills | With Skills |
|--------|---------------|-------------|
| Build an ETL pipeline | Generic PySpark code | Proper SDP with medallion architecture, serverless, quality checks |
| Create a Knowledge Assistant | Copy-paste UI screenshots | `create_or_update_ka()` with right params in seconds |
| Set up a Genie Space | Manual UI steps | Automated with certified queries and sample questions |
| Evaluate agent quality | Guess at metrics | MLflow experiment with industry-standard scorers |
| Schedule workflows | Manual Jobs UI | Multi-task DAG with notifications |

The skills don't replace your judgment — they give your AI assistant the Databricks expertise to execute your ideas correctly the first time.

---

## What's Next

You've completed the full build-a-thon! Here's how to keep going:

1. **Export your agents** — each AgentBricks agent has a model serving endpoint you can call via REST API from any application
2. **Connect real data** — swap the Mag 7 PDFs for your firm's actual filings and internal reports
3. **Add more skills** — create custom skills for your firm's data models, naming conventions, and workflows
4. **Build a Databricks App** — use the `databricks-app-python` skill to wrap your agents in a web interface (Streamlit, Dash, or FastAPI)
5. **Monitor in production** — use the `mlflow-evaluation` skill to set up ongoing quality scoring

**Resources:**
- AI Dev Kit: `https://github.com/databricks-solutions/ai-dev-kit`
- AgentBricks docs: `https://docs.databricks.com/en/generative-ai/agent-bricks/index.html`
- Spark Declarative Pipelines: `https://docs.databricks.com/aws/en/ldp/`
