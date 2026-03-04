# Lab 3 — Data Ingestion

**Time:** ~30 minutes
**Goal:** Land raw finance data into Delta tables using five different ingestion methods — from manual CSV uploads to AI-assisted pipeline generation.

---

## Overview

| Method | Best For | Skill Level |
|--------|----------|-------------|
| **Manual Upload → Auto Loader** | CSVs, Excel exports, one-time loads | Beginner |
| **Extend the Assistant with Agent Skills** | Domain-specific workflows, reusable ETL scripts | Intermediate |
| **Lakeflow Connect (SharePoint/GDrive)** | Live SharePoint/OneDrive data | Intermediate |
| **AI Dev Kit** | Prompt-driven pipeline generation | Advanced |
| **Databricks Assistant for Data Cleaning** | Interactive data cleaning and transformation | Beginner |

## Data We're Ingesting

- `pnl_raw.csv` — P&L across segments and regions
- `budget_vs_actual_raw.csv` — Cost center budgets
- `treasury_loans_raw.csv` — Loan and facility data
- `customer_product_dim_raw.csv` — Customer/product master
- `purchase_requests_emails.txt` — Unstructured email data
- `earnings_call_transcript_excerpt.txt` — Earnings call text

---

## Step 0 — Configuration: Set Your Catalog and Schema

Define your catalog and schema once here. All code throughout the lab references these variables.

```python
# Update these values to match your Unity Catalog setup
CATALOG = "main"             # e.g. "main" or your custom catalog name
SCHEMA  = "finance_workshop" # e.g. "finance_workshop" or your schema name

VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/csv"

print(f"Catalog     : {CATALOG}")
print(f"Schema      : {SCHEMA}")
print(f"Volume path : {VOLUME_PATH}")
```

Then create the schema and volume:

```python
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.raw")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.csv")

print(f"Catalog, schema, and volume ready: {CATALOG}.{SCHEMA} ✓")
```

---

## Method 1 — Manual Upload via UI → Auto Loader

**Who this is for:** Anyone with a CSV or Excel export. No code needed to upload — Auto Loader handles the rest.

### Step 1 — Upload Files in the UI

1. Go to **Catalog** → your catalog → your schema → **Volumes** → `csv`
2. Click **Upload to this volume**
3. Upload all 4 CSV files and 2 text files from the workshop repo `/data/` folder

### Step 2 — Verify the Upload

```python
files = dbutils.fs.ls(VOLUME_PATH)
print(f"Files in volume ({len(files)} total):")
for f in files:
    size_kb = round(f.size / 1024, 1)
    print(f"  {f.name:<55} {size_kb:>8} KB")
```

### Step 3 — Ingest CSVs with Auto Loader

Auto Loader (`cloudFiles`) incrementally ingests files as they land. It handles schema inference, bad records, and new files automatically — no manual schema definition needed.

```python
from pyspark.sql import functions as F

pnl_raw = (
    spark.read
         .format("csv")
         .option("header", "true")
         .option("inferSchema", "false")   # keep everything as string — clean in notebook 02
         .option("multiLine", "true")
         .option("escape", '"')
         .load(f"{VOLUME_PATH}/pnl_raw.csv")
)

print(f"P&L rows loaded    : {pnl_raw.count()}")
print(f"Columns            : {len(pnl_raw.columns)}")
pnl_raw.printSchema()
display(pnl_raw.limit(5))
```

### Step 4 — Ingest All 4 CSVs and Write to Delta

```python
datasets = {
    "pnl_raw":                    "pnl_raw.csv",
    "budget_vs_actual_raw":       "budget_vs_actual_raw.csv",
    "treasury_loans_raw":         "treasury_loans_raw.csv",
    "customer_product_dim_raw":   "customer_product_dim_raw.csv",
}

for table_name, filename in datasets.items():
    df = (
        spark.read
             .format("csv")
             .option("header", "true")
             .option("inferSchema", "false")
             .option("multiLine", "true")
             .option("escape", '"')
             .load(f"{VOLUME_PATH}/{filename}")
    )
    full_table = f"{CATALOG}.{SCHEMA}.{table_name}"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(full_table)
    print(f"✓  {full_table:<55} {df.count():>5} rows")

print("\n✅ All raw structured tables written to Unity Catalog.")
```

---

## Method 2 — Extend the Assistant with ETL Best Practices Skill

**Who this is for:** Teams building production ETL pipelines who need guidance on best practices. The Databricks Assistant — enhanced with a domain-specific skill — provides expert recommendations on Auto Loader, deduplication, MERGE operations, and Delta optimizations.

> This method uses the **ETL Best Practices** skill added to your `.assistant/skills/` folder in the workspace.

### Assistant Prompt

```
I need to build an ETL pipeline that ingests CSV files,
deduplicates records, and writes to a Delta table.
What are the best practices I should follow?
```

**What the Assistant provides (from your skill):**
- Auto Loader configuration with schema inference
- Deduplication strategies (window functions, content hashing)
- MERGE operations for idempotent upserts
- Delta optimization techniques (Z-Order, compaction, vacuum)
- Error handling and monitoring patterns

---

## Method 3 — Lakeflow Connect: Live SharePoint / GDrive Ingestion

**Who this is for:** Finance teams who maintain their source-of-truth in SharePoint/OneDrive. Lakeflow Connect creates a **live, automatically refreshing** pipeline — no manual exports ever again.

### Architecture

```
SharePoint / OneDrive / Google Drive
    │  (OAuth 2.0 — set up once)
    ▼
Lakeflow Connect Pipeline
    │  (incremental, scheduled or triggered)
    ▼
Unity Catalog Delta Table  ──→  Genie  ──→  AI Agents
```

Refer to the official Databricks documentation to set up and configure a Lakeflow Connect pipeline for your source:

- **SharePoint / OneDrive:** [Connect to Microsoft SharePoint](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/sharepoint)
- **Google Drive:** [Connect to Google Drive](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/google-drive)
- **General Lakeflow Connect overview:** [Lakeflow Connect documentation](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/index.html)

---

## Method 4 — AI Dev Kit: Prompt-Driven Pipeline Building

**Who this is for:** Python users who want to build reusable pipelines fast without writing boilerplate from scratch.

The [AI Dev Kit](https://github.com/databricks-solutions/ai-dev-kit) lets you describe what you want in plain English and generates Databricks-ready code.

### Example Prompts

```
"Create a Delta table from this CSV that auto-refreshes every hour"

"Build a pipeline that reads PDF files from a volume and extracts text into a table"

"Write a DLT pipeline that reads this CSV and writes a clean Gold table"

"Generate a streaming pipeline that reads from Kafka and lands in Unity Catalog"
```

### Ingest Unstructured Text Files

```python
from pyspark.sql import functions as F

text_files = [
    "purchase_requests_emails.txt",
    "earnings_call_transcript_excerpt.txt",
]

rows = []
for filename in text_files:
    path = f"{VOLUME_PATH}/{filename}"
    content = dbutils.fs.head(path, 1_000_000)   # read up to 1MB
    rows.append((filename, content))

docs_df = spark.createDataFrame(rows, ["filename", "content"]) \
    .withColumn("word_count",   F.size(F.split(F.col("content"), r"\s+"))) \
    .withColumn("char_count",   F.length(F.col("content"))) \
    .withColumn("ingested_at",  F.current_timestamp())

docs_df.write.mode("overwrite").saveAsTable(f"{CATALOG}.{SCHEMA}.unstructured_docs_raw")
print(f"✓ Ingested {docs_df.count()} documents into {CATALOG}.{SCHEMA}.unstructured_docs_raw")
display(docs_df.select("filename", "word_count", "char_count", "ingested_at"))
```

### AI Dev Kit — Generate a DLT Pipeline Scaffold

```python
import dlt
from pyspark.sql import functions as F

@dlt.table(comment="Raw P&L data from volume — bronze layer")
def pnl_bronze():
    return (
        spark.read.format("csv")
             .option("header", "true")
             .option("inferSchema", "false")
             .load(f"/Volumes/{CATALOG}/{SCHEMA}/raw/pnl_raw.csv")
    )

@dlt.table(comment="Cleaned P&L — silver layer")
@dlt.expect_or_drop("valid_revenue", "revenue_amount IS NOT NULL")
def pnl_silver():
    return (
        dlt.read("pnl_bronze")
           .withColumn("revenue_amount",
               F.regexp_replace(F.col("Revenue"), r"[$,M]", "").cast("double") *
               F.when(F.col("Revenue").contains("M"), 1e6).otherwise(1.0))
    )

@dlt.table(comment="Gold P&L — aggregated by segment and period")
def pnl_gold():
    return (
        dlt.read("pnl_silver")
           .groupBy("Business_Segment", "Period")
           .agg(F.sum("revenue_amount").alias("total_revenue_usd"))
    )
```

To deploy: go to **Workflows → Delta Live Tables → Create Pipeline** → paste this code.

---

## Method 5 — Databricks Assistant for Data Cleaning

**Who this is for:** Anyone who needs to clean messy data interactively. The Databricks Assistant can help process columns, standardize formats, and extract structured data.

### Example: Clean Revenue Column

**Task:** The `Revenue` column contains mixed formats:
- Currency symbols and codes (USD, JPY, SGD, EUR, $, ¥, €)
- Commas in numbers (1,347)
- Million suffixes (0.0M, 3.5M)
- Inconsistent decimal places

**Assistant Prompt:**
```
Read pnl_raw.csv and process the Revenue column:
- Extract currency symbols/codes into a separate column
- Convert text to actual numbers (handle commas, M suffix)
- Keep 2 decimal places
```

### Example: Standardize Business Segments

**Task:** The `Business_Segment` column has 24 variations of the same 4 categories:
- "Prof-Svcs", "Prof. Services", "PROF_SVC", "PS" → Professional Services
- "SW & Svcs", "software and services", "SWS" → Software & Services
- "Compute HW", "COMPUTE_HW", "CHW" → Compute Hardware
- "Cloud-Platform", "CP", "CLOUD_PLAT" → Cloud Platform

**Assistant Prompt:**
```
Classify all business_segment values into distinct and similar categories
```

---

## Final — Verify Tables in Unity Catalog

```python
try:
    tables = spark.sql(f"SHOW TABLES IN {CATALOG}.{SCHEMA}").collect()
except Exception as e:
    print(f"Error: {e}")
    tables = []

print("=" * 60)
print(f" Unity Catalog: {CATALOG}.{SCHEMA}")
print("=" * 60)
for t in tables:
    tname = t["tableName"]
    try:
        count = spark.table(f"{CATALOG}.{SCHEMA}.{tname}").count()
        print(f"  {tname:<45} {count:>6} rows")
    except Exception as e:
        print(f"  {tname:<45}  (error: {e})")

print("\n✅ All tables ready.")
print("   Next: Notebook 02 — ai_parse to normalize and structure the raw data")
```

---

## Next Steps

- **Lab 4** — Information Extraction Agent: parse unstructured text from emails and transcripts
- **Lab 5** — Custom LLM Agent: build a finance Q&A agent over your Delta tables
