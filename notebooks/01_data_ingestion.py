# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Data Ingestion: Landing Raw Finance Data in Databricks
# MAGIC
# MAGIC ## Overview
# MAGIC This notebook shows **three ways** finance teams can get data into Databricks,
# MAGIC regardless of where it lives today:
# MAGIC
# MAGIC | Method | Best For | Skill Level |
# MAGIC |--------|----------|-------------|
# MAGIC | **Manual Upload → Auto Loader** | CSVs, Excel exports, one-time loads | Beginner |
# MAGIC | **Lakeflow Connect (SharePoint)** | Live SharePoint/OneDrive data | Intermediate |
# MAGIC | **AI Dev Kit + Cursor** | Building reusable pipelines fast | Advanced |
# MAGIC
# MAGIC ## Data We're Ingesting
# MAGIC - `pnl_raw.csv` — P&L across segments and regions
# MAGIC - `budget_vs_actual_raw.csv` — Cost center budgets
# MAGIC - `treasury_loans_raw.csv` — Loan and facility data
# MAGIC - `customer_product_dim_raw.csv` — Customer/product master
# MAGIC - `purchase_requests_emails.txt` — Unstructured email data
# MAGIC - `earnings_call_transcript_excerpt.txt` — Earnings call text

# COMMAND ----------

# DBTITLE 1,0 — Setup: Create catalog, schema, and volume
# MAGIC
# MAGIC %sql
# MAGIC -- Run once to set up the workshop namespace
# MAGIC CREATE CATALOG IF NOT EXISTS main;
# MAGIC CREATE SCHEMA IF NOT EXISTS main.finance_workshop;
# MAGIC
# MAGIC -- Volume for raw file landing zone (like an S3 bucket you can browse in the UI)
# MAGIC CREATE VOLUME IF NOT EXISTS main.finance_workshop.raw;
# MAGIC
# MAGIC SELECT 'Catalog, schema, and volume ready ✓' AS status;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Method 1 — Manual Upload via UI → Auto Loader
# MAGIC
# MAGIC **Who this is for:** Anyone with a CSV or Excel export.
# MAGIC No code needed to upload. Auto Loader handles the rest.
# MAGIC
# MAGIC ### Step 1: Upload files in the UI
# MAGIC 1. Go to **Catalog** → `main` → `finance_workshop` → `Volumes` → `raw`
# MAGIC 2. Click **Upload to this volume**
# MAGIC 3. Upload all 4 CSV files and 2 text files from the workshop repo `/data/` folder
# MAGIC
# MAGIC ### Step 2: Verify the upload

# COMMAND ----------

# DBTITLE 1,1a — Verify files landed in the volume

import os
volume_path = "/Volumes/cp_catalog/nvidia/csv"

files = dbutils.fs.ls(volume_path)
print(f"Files in volume ({len(files)} total):")
for f in files:
    size_kb = round(f.size / 1024, 1)
    print(f"  {f.name:<55} {size_kb:>8} KB")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 3: Ingest CSVs with Auto Loader
# MAGIC
# MAGIC Auto Loader (`cloudFiles`) incrementally ingests files as they land.
# MAGIC It handles schema inference, bad records, and new files automatically —
# MAGIC no manual schema definition needed.

# COMMAND ----------

# DBTITLE 1,1b — Ingest P&L CSV with Auto Loader (schema inference)

from pyspark.sql import functions as F

# Auto Loader: reads CSVs in the volume, infers schema, handles new files automatically
pnl_raw = (
    spark.read
         .format("csv")
         .option("header", "true")
         .option("inferSchema", "false")   # keep everything as string — we'll clean in notebook 02
         .option("multiLine", "true")
         .option("escape", '"')
         .load(f"/Volumes/cp_catalog/nvidia/csv/pnl_raw.csv")
)

print(f"P&L rows loaded    : {pnl_raw.count()}")
print(f"Columns            : {len(pnl_raw.columns)}")
print(f"Schema (all string - intentional):")
pnl_raw.printSchema()
display(pnl_raw.limit(5))

# COMMAND ----------

# DBTITLE 1,1c — Ingest all 4 structured CSVs and write to raw Delta tables

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
             .load(f"{volume_path}/{filename}")
    )
    full_table = f"main.finance_workshop.{table_name}"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(full_table)
    print(f"✓  {full_table:<55} {df.count():>5} rows")

print("\n✅ All raw structured tables written to Unity Catalog.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Method 2 — Lakeflow Connect: Live SharePoint, GDrive Ingestion
# MAGIC Notebooks to show 
# MAGIC https://dogfood.staging.databricks.com/editor/notebooks/3064659049279702?o=6051921418418893
# MAGIC
# MAGIC **Who this is for:** Finance teams who maintain their source-of-truth in SharePoint/OneDrive.
# MAGIC Lakeflow Connect creates a **live, automatically refreshing** pipeline — no manual exports ever again.
# MAGIC
# MAGIC ### Architecture
# MAGIC ```
# MAGIC SharePoint / OneDrive
# MAGIC     │  (OAuth 2.0 — set up once)
# MAGIC     ▼
# MAGIC Lakeflow Connect Pipeline
# MAGIC     │  (incremental, scheduled or triggered)
# MAGIC     ▼
# MAGIC Unity Catalog Delta Table  ──→  Genie  ──→  AI Agents
# MAGIC ```

# COMMAND ----------

# Read all PDF files from SharePoint as binary files
# This is a batch read. For automatic incremental ingestion, view the cells at the bottom of the notebook to see how to use this connector in Lakeflow Spark Declarative Pipelines
pdf_df = (spark.read
    .format("binaryFile") # Use this format for unstructured data
    .option("databricks.connection", "brickfood_sharepoint_connection") # User provides the name of their connection
    .option("recursiveFileLookup", True)
    .option("pathGlobFilter", "*.pdf")  # Only ingest PDF files
    .load("https://databricks977.sharepoint.com/sites/brickfood-demo-site/Shared%20Documents/Forms/AllItems.aspx")
    .select("*", "_metadata")
)

# Save the PDF files to a Delta table for persistent storage
pdf_df.write \
    .mode("overwrite") \
    .saveAsTable("aircraft_maintence_logs")

# Display the DataFrame to see the PDF files
display(pdf_df)

# COMMAND ----------

# DBTITLE 1,2b — Create Lakeflow Connect pipeline for SharePoint
# MAGIC
# MAGIC %sql
# MAGIC -- Step 2: Create the pipeline pointing at a specific SharePoint list or library
# MAGIC -- This syncs the SharePoint data into a Unity Catalog table automatically.
# MAGIC
# MAGIC CREATE PIPELINE IF NOT EXISTS finance_sharepoint_budget_pipeline
# MAGIC AS SELECT *
# MAGIC FROM READ_FILES(
# MAGIC   'sharepoint://finance_sharepoint_conn/sites/Finance/Shared Documents/FY24 Budget/',
# MAGIC   format => 'csv',
# MAGIC   header => true
# MAGIC )
# MAGIC INTO main.finance_workshop.budget_sharepoint_live;
# MAGIC
# MAGIC -- Run the pipeline:
# MAGIC -- EXECUTE PIPELINE finance_sharepoint_budget_pipeline;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest Google Drive CSVs with Auto Loader

# COMMAND ----------

df = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("databricks.connection", "my_gdrive_conn")
        .option("pathGlobFilter", "*.csv")
        .option("inferColumnTypes", True)
        .option("header", True)
        .load("https://drive.google.com/drive/folders/1F1gsYmcU4VODUHGppUQdDIgFRYkZW-Fg")
)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Demo Simulation (no SharePoint needed)
# MAGIC For the workshop, we simulate the SharePoint output by reading from the volume.
# MAGIC The schema and behavior are identical to a live Lakeflow Connect pipeline.

# COMMAND ----------

# DBTITLE 1,2c — Simulate SharePoint pipeline output

# Simulate what Lakeflow Connect would deliver — same result, no credentials needed for demo
sharepoint_sim = spark.table("main.finance_workshop.budget_vs_actual_raw") \
    .withColumn("_ingestion_source", F.lit("sharepoint://Finance/FY24 Budget/")) \
    .withColumn("_ingested_at", F.current_timestamp()) \
    .withColumn("_pipeline", F.lit("finance_sharepoint_budget_pipeline"))

sharepoint_sim.write.mode("overwrite").saveAsTable("main.finance_workshop.budget_sharepoint_simulated")
print(f"✓ Simulated SharePoint ingestion: {sharepoint_sim.count()} rows")
print("  In production: this table auto-refreshes whenever SharePoint changes.")
display(sharepoint_sim.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Method 3 — AI Dev Kit: Prompt-Driven Pipeline Building
# MAGIC
# MAGIC **Who this is for:** Python users who want to build reusable pipelines fast
# MAGIC without writing boilerplate from scratch.
# MAGIC
# MAGIC The [AI Dev Kit](https://github.com/databricks-solutions/ai-dev-kit) lets you
# MAGIC describe what you want in plain English, and generates Databricks-ready code.
# MAGIC
# MAGIC ### Setup (run once)
# MAGIC ```bash
# MAGIC pip install databricks-ai-dev-kit
# MAGIC ```
# MAGIC
# MAGIC Or use the Databricks VS Code extension / Cursor with the AI Dev Kit MCP server.
# MAGIC
# MAGIC ### Example prompts you can use right now:
# MAGIC ```
# MAGIC "Create a Delta table from this CSV that auto-refreshes every hour"
# MAGIC
# MAGIC "Build a pipeline that reads PDF files from a volume and extracts text into a table"
# MAGIC
# MAGIC "Write a DLT pipeline that reads this CSV and writes a clean Gold table"
# MAGIC
# MAGIC "Generate a streaming pipeline that reads from Kafka and lands in Unity Catalog"
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,3a — AI Dev Kit: ingest unstructured text files into a table

# This is the code AI Dev Kit generates when you prompt:
# "Read all .txt files from my volume and create a table with filename and full text content"

text_files = [
    "purchase_requests_emails.txt",
    "earnings_call_transcript_excerpt.txt",
]

rows = []
for filename in text_files:
    path = f"{volume_path}/{filename}"
    content = dbutils.fs.head(path, 1_000_000)   # read up to 1MB
    rows.append((filename, content))

docs_df = spark.createDataFrame(rows, ["filename", "content"]) \
    .withColumn("word_count",   F.size(F.split(F.col("content"), r"\s+"))) \
    .withColumn("char_count",   F.length(F.col("content"))) \
    .withColumn("ingested_at",  F.current_timestamp())

docs_df.write.mode("overwrite").saveAsTable("main.finance_workshop.unstructured_docs_raw")
print(f"✓ Ingested {docs_df.count()} documents into main.finance_workshop.unstructured_docs_raw")
display(docs_df.select("filename", "word_count", "char_count", "ingested_at"))

# COMMAND ----------

# DBTITLE 1,3b — AI Dev Kit: generate a DLT pipeline scaffold with a prompt

# AI Dev Kit can also scaffold full DLT pipelines. Example output from the prompt:
# "Write a DLT pipeline that reads pnl_raw.csv and produces a clean gold table"

# This is what AI Dev Kit generates:
dlt_scaffold = '''
import dlt
from pyspark.sql import functions as F

@dlt.table(comment="Raw P&L data from volume — bronze layer")
def pnl_bronze():
    return (
        spark.read.format("csv")
             .option("header", "true")
             .option("inferSchema", "false")
             .load("/Volumes/main/finance_workshop/raw/pnl_raw.csv")
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
'''

print("AI Dev Kit generated DLT pipeline scaffold:")
print(dlt_scaffold)
print("\nTo deploy: go to Workflows → Delta Live Tables → Create Pipeline → paste this code")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary: What We Have in Unity Catalog

# COMMAND ----------

# DBTITLE 1,Final — Inventory all tables created

tables = spark.sql("SHOW TABLES IN main.finance_workshop").collect()
print("=" * 60)
print(" Unity Catalog: main.finance_workshop")
print("=" * 60)
for t in tables:
    tname = t["tableName"]
    try:
        count = spark.table(f"main.finance_workshop.{tname}").count()
        print(f"  {tname:<45} {count:>6} rows")
    except Exception as e:
        print(f"  {tname:<45}  (error: {e})")

print("\n✅ All tables ready.")
print("   Next: Notebook 02 — ai_parse to normalize and structure the raw data")
print("   Then: Notebook 03 — Genie Space + Knowledge Assistant setup")
