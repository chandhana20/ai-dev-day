# Lab 0b — Data Ingestion: From PDFs to Delta Tables

**Time:** ~30 minutes
**Goal:** Land the raw PDF data into Delta tables that the AgentBricks labs depend on. You will do this three ways: (1) run the pre-built notebook using **Databricks Assistant** to understand and extend it, (2) use the **Data Science Agent** to generate code, and (3) use the **AI Dev Kit** to scaffold a production-grade ETL pipeline with Spark Declarative Pipelines.

---

## Why This Lab Matters

The agent labs (Labs 1–5) all depend on structured Delta tables derived from the raw PDFs. This lab is where those tables get created. You'll also learn how to use Databricks AI tools to write data engineering code yourself — so you can adapt this for your own firm's data.

---

## Architecture

```
/Volumes/main/cp_nvidia/
  ├── 10k/               (raw PDFs)
  ├── 10q/               (raw PDFs)
  ├── call_transcripts/  (raw PDFs)
  ├── earning_releases/  (raw PDFs)
  └── annual_report/     (raw PDFs)
         │
         ▼
  [ETL Pipeline — this lab]
         │
         ▼
  main.cp_nvidia.10k_parsed          ← text extracted from 10-Ks
  main.cp_nvidia.call_transcripts_parsed  ← text from transcripts
  main.cp_nvidia.ticker_data_mag7    ← stock price time series
```

---

## Part A — Run the Pre-Built Notebook with Databricks Assistant

### Step 1 — Import the Notebook

1. In the left sidebar, click **Workspace**.
2. Navigate to your user folder: **Workspace → Users → [your email]**
3. Click the **⋮** menu → **Import**.
4. Select **URL** and paste:
   ```
   https://raw.githubusercontent.com/chandhana-padmanabhan_data/ai-dev-day/main/notebooks/01_data_ingestion.py
   ```
5. Click **Import**. The notebook opens automatically.

---

### Step 2 — Explore with Databricks Assistant

Databricks Assistant is built into every notebook. Click the **Assistant** panel (sparkle ✨ icon in the top right of any cell).

Try these prompts in the Assistant to understand the notebook before running it:

> "Explain what this cell does"
*(Select any cell first, then ask)*

> "What does Auto Loader do differently from a regular spark.read?"

> "How would I modify this to also ingest Excel files from the volume?"

> "Add error handling to the CSV ingestion cell that logs bad rows to a separate table"

The Assistant will explain, modify, or generate code inline. Click **Accept** to apply changes to the cell.

---

### Step 3 — Update the Volume Path

Before running, update the volume path to match your workspace:

1. Find the cell with:
   ```python
   volume_path = "/Volumes/cp_catalog/nvidia/csv"
   ```
2. Change it to:
   ```python
   volume_path = "/Volumes/main/cp_nvidia/10k"
   ```
3. Use **Databricks Assistant** to help: select the cell and ask:
   > "Update this notebook to use the volume path /Volumes/main/cp_nvidia/10k and the schema main.cp_nvidia"

---

### Step 4 — Run the Notebook

1. At the top, attach to a cluster (use **Serverless** if available, otherwise select any running cluster).
2. Click **Run All** (or `Shift+Enter` cell by cell to follow along).
3. The notebook will:
   - Create the `main.cp_nvidia` schema if it doesn't exist
   - Read PDFs from the volume
   - Extract text content into rows
   - Write parsed tables to Unity Catalog

4. After completion, verify in the Catalog:
   - Go to **Catalog → main → cp_nvidia → Tables**
   - Confirm `10k_parsed` and `call_transcripts_parsed` appear

---

## Part B — Use the Data Science Agent to Extend the Pipeline

The Databricks **Data Science Agent** can write full notebook sections from a plain English description.

### Step 1 — Open the Data Science Agent

1. In your notebook, click **AI** in the toolbar → **Data Science Agent**.
2. The agent panel opens on the right.

### Step 2 — Ask It to Generate a New Section

Type this prompt:

> "Write a new notebook section that reads all PDF files from /Volumes/main/cp_nvidia/earning_releases, extracts the text from each PDF using pdfplumber or PyMuPDF, creates a Spark DataFrame with columns: filename, company_name (extracted from filename), doc_type='earning_release', text_content, word_count, and ingested_at. Write the result to main.cp_nvidia.earning_releases_parsed."

The agent will:
- Generate the full PySpark code
- Explain what each section does
- Offer to insert it directly into your notebook

Click **Insert into Notebook**, then run the new cell.

### Step 3 — Iterate with the Agent

After running, ask follow-up questions:

> "The company_name extraction didn't work for files like 'AMZN-Q1-2025-Earnings-Release.pdf'. Fix the regex to extract the ticker symbol from the start of the filename."

> "Add a data quality check that flags any rows where word_count is less than 100."

This is the core of AI-assisted data engineering: describe what you want, review the code, run it, and iterate.

---

## Part C — AI Dev Kit: Build a Production ETL Pipeline

The **AI Dev Kit** gives your AI coding assistant (Claude Code, Cursor, etc.) deep knowledge of Databricks patterns through **skills**. Here you'll use it to scaffold a proper Spark Declarative Pipeline (the modern replacement for Delta Live Tables).

### What the AI Dev Kit Does

```
Your prompt (plain English)
        +
AI Dev Kit Skill (Databricks best practices)
        ↓
Production-ready pipeline code
        ↓
Auto-deployed to your workspace
```

### Step 1 — Set Up the AI Dev Kit

Open a **Terminal** on your laptop (not inside Databricks) and run:

```bash
git clone https://github.com/databricks-solutions/ai-dev-kit.git
cd ai-dev-kit/ai-dev-project
./setup.sh
```

When prompted:
- **Databricks host**: `https://e2-demo-west.cloud.databricks.com`
- **Profile**: `e2-demo-west`

This installs the skills and MCP server, then opens Claude Code pre-configured for Databricks.

### Step 2 — Install the Spark Declarative Pipelines Skill

If you already have Claude Code open without the full setup:

```bash
cd ai-dev-kit
./databricks-skills/install_skills.sh
```

This copies all skills into `.claude/skills/` — Claude Code loads them automatically.

### Step 3 — Prompt Claude Code to Build Your Pipeline

With Claude Code open (run `claude` in the ai-dev-kit project directory), type:

```
Build a Spark Declarative Pipeline for the NVIDIA Finance Build-a-Thon that:

Bronze layer:
- Reads all PDF files from /Volumes/main/cp_nvidia/10k/ as binary files
- Extracts file metadata (filename, file_size, ingested_at)
- Writes to main.cp_nvidia.bronze_10k_files

Silver layer:
- Reads bronze_10k_files
- Extracts text content from each PDF using pdf parsing
- Parses the company ticker from the filename
- Adds doc_type = '10k'
- Applies a data quality expectation: drop rows where text_content is NULL
- Writes to main.cp_nvidia.silver_10k_parsed

Gold layer:
- Reads silver_10k_parsed
- Computes word_count, unique_words, and estimated_pages per document
- Groups by company ticker with document count
- Writes to main.cp_nvidia.gold_10k_summary

Use the catalog main and schema cp_nvidia. Use serverless compute.
```

Claude Code will:
1. Load the `spark-declarative-pipelines` skill automatically
2. Initialize a proper pipeline project with Asset Bundles
3. Write the bronze/silver/gold SQL/Python files
4. Upload them to your workspace
5. Create and run the pipeline
6. Verify the output tables

### Step 4 — Watch the Pipeline Run

1. In Databricks, go to **Workflows → Delta Live Tables** (or **Lakeflow Pipelines**).
2. Find `nvidia-finance-etl-pipeline`.
3. Click into it — you'll see the live DAG showing bronze → silver → gold flowing.
4. Wait for status to show **Completed**.

### Step 5 — Verify the Output Tables

```sql
-- In the Databricks SQL Editor:
SELECT company_ticker, word_count, estimated_pages
FROM main.cp_nvidia.gold_10k_summary
ORDER BY company_ticker;
```

You should see one row per company (AAPL, AMZN, GOOG, META, MSFT, NVDA, TSLA).

---

## Part D — Schedule the Pipeline (Optional)

For a real deployment, you want new filings to be processed automatically:

1. In Claude Code, type:
   ```
   Add a daily schedule to the nvidia-finance-etl-pipeline so it runs at 7am UTC
   ```

2. Or in Databricks UI: go to your pipeline → **Settings** → **Trigger** → **Scheduled** → set frequency.

---

## Summary

You now have three tools in your toolkit for data ingestion:

| Tool | Best For |
|------|----------|
| **Databricks Assistant** | Understanding existing code, making quick edits in notebooks |
| **Data Science Agent** | Generating new notebook sections from plain English descriptions |
| **AI Dev Kit + SDP** | Scaffolding production-grade ETL pipelines with bronze/silver/gold architecture |

All three feed into the same output: clean Delta tables in `main.cp_nvidia` that power the agents you build in Labs 1–5.

**Next:** [Lab 1 — Information Extraction Agent](01-information-extraction-agent.md)
