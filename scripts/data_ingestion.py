"""
Bluestock MF Capstone — ETL Pipeline (Ingestion & Data Quality Report)

Loads all 10 raw CSV files, prints schema info (shape, dtypes, head),
validates AMFI code referential integrity, and outputs a data quality report.
"""

import sys
from pathlib import Path
import pandas as pd


# -- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Ordered list of raw CSVs (filename -> friendly label)
RAW_FILES = {
    "01_fund_master.csv":           "Fund Master",
    "02_nav_history.csv":           "NAV History",
    "03_aum_by_fund_house.csv":     "AUM by Fund House",
    "04_monthly_sip_inflows.csv":   "Monthly SIP Inflows",
    "05_category_inflows.csv":      "Category Inflows",
    "06_industry_folio_count.csv":  "Industry Folio Count",
    "07_scheme_performance.csv":    "Scheme Performance",
    "08_investor_transactions.csv": "Investor Transactions",
    "09_portfolio_holdings.csv":    "Portfolio Holdings",
    "10_benchmark_indices.csv":     "Benchmark Indices",
}


def load_all_csvs() -> dict:
    """Load every raw CSV into a dict keyed by filename (without extension)."""
    dataframes = {}
    for filename, label in RAW_FILES.items():
        filepath = RAW_DIR / filename
        if not filepath.exists():
            print(f"  [WARN] {label} ({filename}) -- FILE NOT FOUND, skipping")
            continue
        df = pd.read_csv(filepath)
        key = filename.replace(".csv", "")
        dataframes[key] = df
        print(f"  [OK]  {label:30s}  shape={str(df.shape):16s}  cols={len(df.columns)}")
    return dataframes


def print_schema_details(dataframes: dict) -> None:
    """Print dtypes and head(3) for every loaded dataset."""
    for key, df in dataframes.items():
        label = RAW_FILES.get(f"{key}.csv", key)
        print(f"\n{'='*72}")
        print(f"  {label}  ({key})")
        print(f"{'-'*72}")
        print(f"  Shape : {df.shape}")
        print(f"  Dtypes:")
        for col in df.columns:
            print(f"    {col:35s}  {str(df[col].dtype)}")
        print(f"\n  head(3):")
        print(df.head(3).to_string(index=False))


def validate_amfi_codes(dataframes: dict) -> None:
    """Check that all AMFI codes in fund_master also appear in nav_history."""
    fund_master = dataframes.get("01_fund_master")
    nav_history = dataframes.get("02_nav_history")

    if fund_master is None or nav_history is None:
        print("  [WARN] Cannot validate -- fund_master or nav_history not loaded")
        return

    master_codes = set(fund_master["amfi_code"].unique())
    nav_codes = set(nav_history["amfi_code"].unique())

    missing = master_codes - nav_codes
    extra = nav_codes - master_codes

    print(f"\n{'='*72}")
    print("  AMFI Code Validation")
    print(f"{'-'*72}")
    print(f"  Codes in fund_master  : {len(master_codes)}")
    print(f"  Codes in nav_history  : {len(nav_codes)}")
    if missing:
        print(f"  [WARN] In master but NOT in NAV history ({len(missing)}): {sorted(missing)}")
    else:
        print(f"  [OK]  All master codes present in nav_history")
    if extra:
        print(f"  [INFO] In NAV history but NOT in master ({len(extra)}): {sorted(extra)}")


def data_quality_report(dataframes: dict) -> None:
    """Print a concise data-quality summary for each dataset."""
    print(f"\n{'='*72}")
    print("  DATA QUALITY REPORT")
    print(f"{'='*72}")
    for key, df in dataframes.items():
        label = RAW_FILES.get(f"{key}.csv", key)
        nulls = df.isnull().sum()
        null_cols = nulls[nulls > 0]
        dupes = df.duplicated().sum()
        print(f"\n  {label}")
        print(f"    Rows: {len(df):,}  |  Cols: {len(df.columns)}  |  Duplicates: {dupes}")
        if len(null_cols):
            print(f"    Null columns:")
            for col, cnt in null_cols.items():
                print(f"      {col}: {cnt} nulls ({cnt/len(df)*100:.1f}%)")
        else:
            print(f"    [OK]  No null values")


def run_ingestion() -> dict:
    """Master entry-point: load, report, validate."""
    print("\n" + "="*72)
    print("       BLUESTOCK MF -- ETL PIPELINE (Ingestion)")
    print("="*72 + "\n")

    print("> Loading raw CSV files ...")
    dataframes = load_all_csvs()

    print_schema_details(dataframes)
    validate_amfi_codes(dataframes)
    data_quality_report(dataframes)

    print(f"\n{'='*72}")
    print(f"  [OK]  Ingestion complete -- {len(dataframes)} datasets loaded")
    print(f"{'='*72}\n")
    return dataframes


# --------------------------------------------------------------------------
if __name__ == "__main__":
    run_ingestion()
