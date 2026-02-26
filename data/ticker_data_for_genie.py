# Databricks notebook source
# MAGIC %md
# MAGIC # Ticker Data for Genie
# MAGIC
# MAGIC This notebook downloads historical stock market data for the **Magnificent 7** companies
# MAGIC and loads it into a Unity Catalog Delta table for use with the Genie Space in Lab 4.
# MAGIC
# MAGIC **Output table:** `catalog.schema.ticker_data_mag7`
# MAGIC
# MAGIC **Companies covered:**
# MAGIC | Ticker | Company |
# MAGIC |--------|---------|
# MAGIC | AAPL | Apple |
# MAGIC | AMZN | Amazon |
# MAGIC | GOOGL | Alphabet (Google) |
# MAGIC | META | Meta Platforms |
# MAGIC | MSFT | Microsoft |
# MAGIC | NVDA | NVIDIA |
# MAGIC | TSLA | Tesla |

# COMMAND ----------

# DBTITLE 1,0 — Install dependencies
# MAGIC %pip install yfinance --quiet
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,1 — Configuration: set your catalog and schema
# Update these to match your Unity Catalog setup
CATALOG = "catalog"   # e.g. "main"
SCHEMA  = "schema"    # e.g. "my_schema"
TABLE   = "ticker_data_mag7"

FULL_TABLE = f"{CATALOG}.{SCHEMA}.{TABLE}"

# Mag 7 tickers and display names
MAG7 = {
    "AAPL":  "Apple",
    "AMZN":  "Amazon",
    "GOOGL": "Alphabet",
    "META":  "Meta",
    "MSFT":  "Microsoft",
    "NVDA":  "NVIDIA",
    "TSLA":  "Tesla",
}

# Date range for historical data
START_DATE = "2022-01-01"
END_DATE   = "2025-12-31"

print(f"Target table : {FULL_TABLE}")
print(f"Date range   : {START_DATE} → {END_DATE}")
print(f"Tickers      : {', '.join(MAG7.keys())}")

# COMMAND ----------

# DBTITLE 1,2 — Create schema if it doesn't exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
print(f"✓ Schema ready: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# DBTITLE 1,3 — Download historical price and fundamental data
import yfinance as yf
import pandas as pd
from datetime import datetime

rows = []

for ticker, company in MAG7.items():
    print(f"Downloading {ticker} ({company})...")
    try:
        stock = yf.Ticker(ticker)

        # Historical daily prices
        hist = stock.history(start=START_DATE, end=END_DATE, auto_adjust=True)
        if hist.empty:
            print(f"  ⚠ No price data for {ticker}")
            continue

        hist = hist.reset_index()
        hist["date"]         = pd.to_datetime(hist["Date"]).dt.date
        hist["company_name"] = ticker
        hist["price_open"]   = hist["Open"].round(4)
        hist["price_close"]  = hist["Close"].round(4)
        hist["volume"]       = hist["Volume"].astype("Int64")

        # Fundamental data (point-in-time from yfinance info)
        info = stock.info
        hist["pe_trailing"]  = info.get("trailingPE")
        hist["pe_forward"]   = info.get("forwardPE")
        hist["ev_ebitda"]    = info.get("enterpriseToEbitda")
        hist["market_cap"]   = info.get("marketCap")
        hist["beta"]         = info.get("beta")

        rows.append(hist[[
            "date", "company_name",
            "price_open", "price_close", "volume",
            "pe_trailing", "pe_forward", "ev_ebitda", "market_cap", "beta"
        ]])
        print(f"  ✓ {len(hist):,} rows")

    except Exception as e:
        print(f"  ✗ Error for {ticker}: {e}")

all_data = pd.concat(rows, ignore_index=True)
print(f"\nTotal rows downloaded: {len(all_data):,}")
display(all_data.head(10))

# COMMAND ----------

# DBTITLE 1,4 — Write to Unity Catalog Delta table
from pyspark.sql.types import (
    StructType, StructField, DateType, StringType,
    DoubleType, LongType
)

schema = StructType([
    StructField("date",         DateType(),   True),
    StructField("company_name", StringType(), False),
    StructField("price_open",   DoubleType(), True),
    StructField("price_close",  DoubleType(), True),
    StructField("volume",       LongType(),   True),
    StructField("pe_trailing",  DoubleType(), True),
    StructField("pe_forward",   DoubleType(), True),
    StructField("ev_ebitda",    DoubleType(), True),
    StructField("market_cap",   LongType(),   True),
    StructField("beta",         DoubleType(), True),
])

sdf = spark.createDataFrame(all_data, schema=schema)

(sdf.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(FULL_TABLE))

count = spark.table(FULL_TABLE).count()
print(f"✓ Written {count:,} rows to {FULL_TABLE}")

# COMMAND ----------

# DBTITLE 1,5 — Verify the table
display(spark.sql(f"""
    SELECT
        company_name,
        MIN(date)         AS earliest_date,
        MAX(date)         AS latest_date,
        COUNT(*)          AS trading_days,
        ROUND(MIN(price_close), 2)  AS min_close,
        ROUND(MAX(price_close), 2)  AS max_close,
        ROUND(AVG(price_close), 2)  AS avg_close
    FROM {FULL_TABLE}
    GROUP BY company_name
    ORDER BY company_name
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC
# MAGIC The table `catalog.schema.ticker_data_mag7` is now ready.
# MAGIC
# MAGIC Use it in **Lab 4 — Genie Space**:
# MAGIC - Add this table to your Genie Space alongside the KIE responses table
# MAGIC - Join on: `ticker_data_mag7.company_name = kie_table.stock_symbol`
# MAGIC
# MAGIC **Sample queries to try in Genie:**
# MAGIC - *"What was NVIDIA's highest closing price in 2024?"*
# MAGIC - *"Which Mag 7 company had the highest trading volume last month?"*
# MAGIC - *"Show me Microsoft's stock price trend over the past year"*
# MAGIC - *"Compare revenue growth vs stock price appreciation across all companies"*
