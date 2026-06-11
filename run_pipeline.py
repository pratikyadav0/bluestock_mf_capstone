"""
Bluestock MF Capstone — Master Pipeline Runner

Orchestrates the full ETL workflow:
  1. Ingest raw CSVs   (scripts/etl_pipeline.py)
  2. Clean all datasets (scripts/data_cleaning.py)
  3. Load into SQLite   (star-schema tables)
  4. Print summary
"""

import sys
import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# -- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR = PROJECT_ROOT / "data" / "db"
DB_PATH = DB_DIR / "bluestock_mf.db"
SQL_DIR = PROJECT_ROOT / "sql"

# Ensure directories exist
DB_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Add project root to sys.path for script imports
sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================================
#  STEP 1 -- INGESTION
# =========================================================================
def step_ingestion():
    from scripts.etl_pipeline import run_ingestion
    return run_ingestion()


# =========================================================================
#  STEP 2 -- CLEANING
# =========================================================================
def step_cleaning():
    from scripts.data_cleaning import run_cleaning
    run_cleaning()


# =========================================================================
#  STEP 3 -- LOAD INTO SQLITE
# =========================================================================

# Map from processed CSV filename -> (table_name, if_exists)
TABLE_MAP = {
    "01_fund_master.csv":           ("dim_fund",                "replace"),
    "02_nav_history.csv":           ("fact_nav",                "replace"),
    "03_aum_by_fund_house.csv":     ("fact_aum",                "replace"),
    "04_monthly_sip_inflows.csv":   ("fact_sip_industry",       "replace"),
    "05_category_inflows.csv":      ("fact_category_inflows",   "replace"),
    "06_industry_folio_count.csv":  ("fact_folio_count",        "replace"),
    "07_scheme_performance.csv":    ("fact_performance",        "replace"),
    "08_investor_transactions.csv": ("fact_transactions",       "replace"),
    "09_portfolio_holdings.csv":    ("fact_portfolio",          "replace"),
    "10_benchmark_indices.csv":     ("fact_benchmark_indices",  "replace"),
}

# Column renames from CSV headers -> schema columns
COLUMN_RENAMES = {
    "fact_nav": {
        "date": "nav_date",
    },
}


def _generate_dim_date(engine) -> None:
    """Programmatically generate dim_date for 2022-01-01 to 2026-05-31."""
    start = datetime.date(2022, 1, 1)
    end = datetime.date(2026, 5, 31)
    dates = pd.date_range(start, end, freq="D")
    df = pd.DataFrame({
        "date_id": dates.strftime("%Y%m%d").astype(int),
        "date": dates.strftime("%Y-%m-%d"),
        "year": dates.year,
        "month": dates.month,
        "quarter": dates.quarter,
        "day_of_week": dates.day_name(),
        "is_weekday": np.where(dates.weekday < 5, 1, 0),
    })
    df.to_sql("dim_date", engine, if_exists="replace", index=False)
    print(f"    -> dim_date: {len(df):,} rows (2022-01-01 to 2026-05-31)")


def _execute_schema(engine) -> None:
    """Execute the schema.sql DDL to create tables and indexes."""
    schema_path = SQL_DIR / "schema.sql"
    if schema_path.exists():
        ddl = schema_path.read_text(encoding="utf-8")
        with engine.begin() as conn:
            for stmt in ddl.split(";"):
                stmt = stmt.strip()
                if stmt:
                    conn.execute(text(stmt))
        print("    -> schema.sql executed")
    else:
        print("    [WARN] schema.sql not found -- tables will be created by pandas")


def step_load_database():
    """Load all cleaned CSVs into the SQLite database."""
    print("\n" + "="*72)
    print("       BLUESTOCK MF -- DATABASE LOADER")
    print("="*72 + "\n")

    engine = create_engine(f"sqlite:///{DB_PATH}")

    # Execute DDL schema first
    _execute_schema(engine)

    # Generate dim_date
    print("  > Generating dim_date ...")
    _generate_dim_date(engine)

    # Load each processed CSV
    for csv_name, (table_name, if_exists) in TABLE_MAP.items():
        csv_path = PROCESSED_DIR / csv_name
        if not csv_path.exists():
            print(f"  [WARN] {csv_name} not found in processed/, skipping")
            continue

        print(f"  > Loading {csv_name} -> {table_name} ...")
        df = pd.read_csv(csv_path)

        # Apply column renames if any
        renames = COLUMN_RENAMES.get(table_name, {})
        if renames:
            df.rename(columns=renames, inplace=True)

        # For fact_transactions, drop tx_id if present (will be auto-generated)
        if table_name == "fact_transactions" and "tx_id" in df.columns:
            df.drop(columns=["tx_id"], inplace=True)

        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        print(f"    -> {table_name}: {len(df):,} rows loaded")

    # Final table summary
    print(f"\n  --- Database Summary ---")
    with engine.connect() as conn:
        tables = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        ).fetchall()
        for (tbl,) in tables:
            cnt = conn.execute(text(f'SELECT COUNT(*) FROM "{tbl}"')).scalar()
            print(f"    {tbl:30s}  {cnt:>10,} rows")

    print(f"\n  [OK]  Database saved to {DB_PATH}\n")


# =========================================================================
#  STEP 4 -- COMPUTE PERFORMANCE METRICS
# =========================================================================
def step_compute_metrics():
    print("\n=== STEP 4: Computing Performance Metrics ===")
    from scripts.compute_metrics import main as run_metrics
    run_metrics()


# =========================================================================
#  STEP 5 -- EXPLORATORY DATA ANALYSIS
# =========================================================================
def step_eda():
    print("\n=== STEP 5: Running Exploratory Data Analysis ===")
    from scripts.eda_analysis import load_data, print_eda_findings
    import scripts.eda_analysis as eda
    data = load_data()
    # Run all chart functions
    chart_funcs = [f for f in dir(eda) if f.startswith('chart_')]
    for fn_name in chart_funcs:
        try:
            fn = getattr(eda, fn_name)
            fn(data)
            print(f"    -> {fn_name} done")
        except Exception as e:
            print(f"    [WARN] {fn_name}: {e}")
    print_eda_findings(data)
    print("  [OK] EDA complete — charts saved to charts/")


# =========================================================================
#  STEP 6 -- ADVANCED ANALYTICS
# =========================================================================
def step_advanced_analytics():
    print("\n=== STEP 6: Running Advanced Analytics ===")
    from scripts.advanced_analytics import main as run_advanced
    run_advanced()


# =========================================================================
#  STEP 7 -- GENERATE DASHBOARD DATA
# =========================================================================
def step_generate_dashboard_data():
    print("\n=== STEP 7: Generating Dashboard JSON Files ===")
    from scripts.generate_dashboard_data import main as run_dashboard_export
    run_dashboard_export()


# =========================================================================
#  STEP 8 -- FUND RECOMMENDATIONS
# =========================================================================
def step_recommender():
    print("\n=== STEP 8: Generating Fund Recommendations ===")
    from scripts.recommender import main as run_recommender
    run_recommender()


# =========================================================================
#  SUMMARY
# =========================================================================
def step_summary():
    print("\n" + "="*72)
    print("       BLUESTOCK MF -- PIPELINE COMPLETE")
    print("="*72)
    print(f"""
    Project Root    : {PROJECT_ROOT}
    Raw Data        : {PROJECT_ROOT / 'data' / 'raw'}
    Processed Data  : {PROCESSED_DIR}
    SQLite Database : {DB_PATH}
    Charts          : {PROJECT_ROOT / 'charts'}
    Dashboard       : {PROJECT_ROOT / 'dashboard'}
    Reports         : {PROJECT_ROOT / 'reports'}
    """)


# =========================================================================
#  MAIN
# =========================================================================
def main():
    print(f"\n{'='*72}")
    print(f"  BLUESTOCK MUTUAL FUND ANALYTICS -- FULL PIPELINE")
    print(f"  Started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*72}")

    # Step 1: Ingestion
    print("\n=== STEP 1: Data Ingestion ===")
    step_ingestion()

    # Step 2: Cleaning
    print("\n=== STEP 2: Data Cleaning ===")
    step_cleaning()

    # Step 3: Load into SQLite
    print("\n=== STEP 3: Loading into SQLite Database ===")
    step_load_database()

    # Step 4: Performance Metrics
    step_compute_metrics()

    # Step 5: EDA
    step_eda()

    # Step 6: Advanced Analytics
    step_advanced_analytics()

    # Step 7: Dashboard Data
    step_generate_dashboard_data()

    # Step 8: Recommendations
    step_recommender()

    # Final Summary
    step_summary()

    print(f"  Finished at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*72}\n")


if __name__ == "__main__":
    main()
