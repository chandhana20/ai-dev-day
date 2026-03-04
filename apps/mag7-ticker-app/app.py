"""
MAG-7 Ticker Data Explorer -- Databricks App (Streamlit)

Reads from Unity Catalog table {CATALOG}.{SCHEMA}.{TABLE} using the
databricks-sql-connector and displays interactive charts and tables
for the Magnificent Seven stocks (AAPL, AMZN, GOOGL, META, MSFT, NVDA, TSLA).

Follows the apps-cookbook tables_read pattern:
  https://apps-cookbook.dev/docs/streamlit/tables/tables_read
"""

import os

import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MAG-7 Ticker Explorer",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Databricks connection (cached, following cookbook pattern)
# ---------------------------------------------------------------------------
cfg = Config()

WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID", "75fd8278393d07eb")
HTTP_PATH = f"/sql/1.0/warehouses/{WAREHOUSE_ID}"

# ---------------------------------------------------------------------------
# Data source configuration — set via environment variables or update defaults
# ---------------------------------------------------------------------------
CATALOG = os.getenv("DATABRICKS_CATALOG", "main")
SCHEMA  = os.getenv("DATABRICKS_SCHEMA", "fins_agent_bricks_demo")
TABLE   = os.getenv("DATABRICKS_TABLE",  "ticker_data_mag7")

TABLE_NAME = f"{CATALOG}.{SCHEMA}.{TABLE}"

# Columns to read (excluding `peg` which has void type)
COLUMNS = (
    "date, company_name, price_open, price_close, volume, "
    "pe_trailing, pe_forward, ev_ebitda, market_cap, beta"
)

TICKER_COLORS = {
    "AAPL": "#A2AAAD",
    "AMZN": "#FF9900",
    "GOOGL": "#4285F4",
    "META": "#0081FB",
    "MSFT": "#7FBA00",
    "NVDA": "#76B900",
    "TSLA": "#CC0000",
}


@st.cache_resource(ttl=300, show_spinner="Connecting to Databricks SQL ...")
def get_connection():
    """Return a reusable DBSQL connection (cached for 5 min)."""
    return sql.connect(
        server_hostname=cfg.host,
        http_path=HTTP_PATH,
        credentials_provider=lambda: cfg.authenticate,
    )


@st.cache_data(ttl=300, show_spinner="Fetching ticker data ...")
def load_data() -> pd.DataFrame:
    """Read the MAG-7 ticker table into a Pandas DataFrame."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNS} FROM {TABLE_NAME} ORDER BY date, company_name")
        df = cursor.fetchall_arrow().to_pandas()

    # Ensure proper types
    df["date"] = pd.to_datetime(df["date"]).dt.date
    for col in ["price_open", "price_close", "pe_trailing", "pe_forward", "ev_ebitda", "beta"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["volume", "market_cap"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
try:
    df = load_data()
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

all_tickers = sorted(df["company_name"].unique().tolist())
min_date = df["date"].min()
max_date = df["date"].max()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("MAG-7 Ticker Data Explorer")
st.caption(
    f"Source: `{TABLE_NAME}`  |  "
    f"{len(df):,} rows  |  "
    f"{min_date} to {max_date}"
)

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.header("Filters")

selected_tickers = st.sidebar.multiselect(
    "Ticker symbols",
    options=all_tickers,
    default=all_tickers,
    help="Select one or more MAG-7 tickers to display",
)

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter rows by date range",
)

sort_col = st.sidebar.selectbox(
    "Sort table by",
    options=["date", "company_name", "price_close", "volume", "market_cap"],
    index=0,
)

sort_asc = st.sidebar.toggle("Ascending", value=True)

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    df["company_name"].isin(selected_tickers)
    & (df["date"] >= start_date)
    & (df["date"] <= end_date)
)
filtered = df.loc[mask].sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
if not filtered.empty:
    cols = st.columns(len(selected_tickers))
    latest = filtered.sort_values("date").groupby("company_name").last()
    for i, ticker in enumerate(selected_tickers):
        if ticker in latest.index:
            row = latest.loc[ticker]
            cols[i].metric(
                label=ticker,
                value=f"${row['price_close']:,.2f}",
                delta=f"{row['price_close'] - row['price_open']:+.2f} (day)",
            )
else:
    st.info("No data matches the current filters.")

st.divider()

# ---------------------------------------------------------------------------
# Closing price chart
# ---------------------------------------------------------------------------
st.subheader("Closing Prices")

if not filtered.empty:
    chart_df = (
        filtered[["date", "company_name", "price_close"]]
        .pivot(index="date", columns="company_name", values="price_close")
    )
    st.line_chart(chart_df, use_container_width=True)
else:
    st.warning("Select at least one ticker to see the chart.")

# ---------------------------------------------------------------------------
# Volume chart
# ---------------------------------------------------------------------------
st.subheader("Trading Volume")

if not filtered.empty:
    vol_df = (
        filtered[["date", "company_name", "volume"]]
        .pivot(index="date", columns="company_name", values="volume")
    )
    st.bar_chart(vol_df, use_container_width=True)

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------
st.subheader("Data Table")

if not filtered.empty:
    st.dataframe(
        filtered,
        use_container_width=True,
        height=450,
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "company_name": st.column_config.TextColumn("Ticker"),
            "price_open": st.column_config.NumberColumn("Open", format="$%.2f"),
            "price_close": st.column_config.NumberColumn("Close", format="$%.2f"),
            "volume": st.column_config.NumberColumn("Volume", format="%d"),
            "pe_trailing": st.column_config.NumberColumn("P/E (TTM)", format="%.2f"),
            "pe_forward": st.column_config.NumberColumn("P/E (Fwd)", format="%.2f"),
            "ev_ebitda": st.column_config.NumberColumn("EV/EBITDA", format="%.2f"),
            "market_cap": st.column_config.NumberColumn("Mkt Cap", format="$%d"),
            "beta": st.column_config.NumberColumn("Beta", format="%.3f"),
        },
    )

    csv = filtered.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="mag7_ticker_data.csv",
        mime="text/csv",
    )
else:
    st.info("No rows to display.")
