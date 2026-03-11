# Lab 2 — Information Extraction

**Time:** ~25 minutes
**Goal:** Use AgentBricks Information Extraction to automatically parse 10-K SEC filings (PDFs) into a structured Delta table — no code required.

**Business Problem:** Finance teams spend hours manually pulling numbers from 10-K filings. Information Extraction does it in minutes — consistently and at scale.

---

## Overview

You will use **AgentBricks → Information Extraction** to:
1. Parse raw PDF documents (10-K filings) into a structured table
2. Build an extraction agent that identifies key financial fields
3. Generate a schema from the parsed data
4. Create the agent and run it at scale

---

## Prerequisites

- A **SQL Warehouse** must be running before you start. If you don't have one:
  - Go to **Compute** in the left sidebar
  - Click **Create** → **SQL Warehouse**
  - Choose a size (Small is fine for this lab) and click **Create**
  - Wait for it to start (green status)

- Your 10-K PDF files should already be uploaded to a Unity Catalog Volume (e.g., `your_catalog.your_schema.10k`)

---

## Step 1 — Parse PDFs into a Table

### 1.1 Navigate to Information Extraction
- In the left sidebar, click **AI/ML** → **Agents**
- Click **Information Extraction**

### 1.2 Select "Use PDFs"
- Click **Use PDFs** as your first step
- This tells AgentBricks you want to extract structured data from PDF documents

### 1.3 Select Your PDF Source Folder
- Browse to the Unity Catalog Volume that contains your 10-K filings
- Example: `your_catalog.your_schema.10k`
- Click to select the folder

### 1.4 Set the Destination Table
- Choose where you want the parsed output to be written
- Select your **catalog** and **schema**
- Enter a table name, e.g., `10k_parsed`
- Full path example: `your_catalog.your_schema.10k_parsed`

### 1.5 Select a SQL Warehouse
- Pick the SQL Warehouse you started in the prerequisites
- **Important:** The warehouse must already be running — it will not auto-start

### 1.6 Start the Import
- Click **Start Import**
- This will take **~15–20 minutes** to process all your PDFs
- AgentBricks reads each PDF, extracts text and structure, and writes the results to your destination table
- You can navigate away and come back — the job runs in the background

### 1.7 Verify the Parsed Table
- Once complete, go to **Catalog** → browse to `your_catalog.your_schema.10k_parsed`
- Click **Sample Data** to confirm the PDFs were parsed correctly

---

## Step 2 — Build the Extraction Agent

### 2.1 Navigate Back to Information Extraction
- Go to **AI/ML** → **Agents** → **Information Extraction**
- Click **Build**

### 2.2 Select Your Parsed Table as the Dataset
- Click **Unlabeled Dataset**
- Go into **Dataset Selection**
- Browse and select the parsed table you created in Step 1 (e.g., `your_catalog.your_schema.10k_parsed`)
- Click **Use This Table**

### 2.3 Generate the Schema
- Wait for the system to process sample documents from your parsed table
- AgentBricks will automatically generate a **sample JSON output** — this is the proposed extraction schema
- Review the generated fields — they should include financial metrics like revenue, net income, total assets, etc.

### 2.4 Choose Your Optimization Strategy
- You will see two options:
  - **Optimize for Scale** — faster and cheaper, best for large volumes of similar documents
  - **Optimize for Complexity** — more accurate on complex or varied documents, costs more per document
- For 10-K filings (standardized format, high volume), **Optimize for Scale** is recommended
- For diverse or unusual document types, choose **Optimize for Complexity**

### 2.5 Create the Agent
- Click **Create Agent**
- AgentBricks builds your extraction agent with the generated schema and optimization settings
- Once created, you can run it against your full document set to populate a structured Delta table

---

## Verify Your Output

Run this in the SQL Editor to confirm extraction worked:

```sql
SELECT *
FROM your_catalog.your_schema.10k_parsed
LIMIT 10;
```

You should see structured rows with extracted financial data from your 10-K filings.

---

## Summary

You built an Information Extraction agent that:
- **Parsed** raw PDF filings into a structured table (no code)
- **Generated** an extraction schema automatically from sample data
- **Created** a reusable agent optimized for your document type

All done through the UI — no coding required.

**Next:** [Lab 3 — Genie Space](02-genie-setup.md)
