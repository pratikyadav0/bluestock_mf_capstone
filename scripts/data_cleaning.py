"""
Bluestock MF Capstone — Data Cleaning

Cleans every raw CSV and writes the result to data/processed/.
Each cleaner is tailored to the column semantics of its dataset.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# -- Helpers ---------------------------------------------------------------

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / name)


def _save(df: pd.DataFrame, name: str) -> None:
    _ensure_dir(PROCESSED_DIR)
    out = PROCESSED_DIR / name
    df.to_csv(out, index=False)
    print(f"    -> saved {out.name}  ({len(df):,} rows)")


# -- Individual cleaners ---------------------------------------------------

def clean_fund_master() -> pd.DataFrame:
    """Clean 01_fund_master.csv: parse dates, strip text, validate numerics."""
    df = _load("01_fund_master.csv")
    df["launch_date"] = pd.to_datetime(df["launch_date"], errors="coerce")
    for col in ["fund_house", "scheme_name", "category", "sub_category",
                 "plan", "benchmark", "fund_manager", "risk_category",
                 "sebi_category_code"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    for col in ["expense_ratio_pct", "exit_load_pct", "min_sip_amount", "min_lumpsum_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.drop_duplicates(subset=["amfi_code"], inplace=True)
    # Convert date back to string for CSV output
    df["launch_date"] = df["launch_date"].dt.strftime("%Y-%m-%d")
    _save(df, "01_fund_master.csv")
    return df


def clean_nav_history() -> pd.DataFrame:
    """Clean 02_nav_history.csv:
    - parse dates, sort, remove dups, validate NAV > 0,
    - compute daily_return_pct
    """
    df = _load("02_nav_history.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df[df["nav"] > 0].copy()
    df.sort_values(["amfi_code", "date"], inplace=True)
    df.drop_duplicates(subset=["amfi_code", "date"], keep="last", inplace=True)
    df["daily_return_pct"] = (
        df.groupby("amfi_code")["nav"]
          .pct_change() * 100
    ).round(4)
    df.reset_index(drop=True, inplace=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    _save(df, "02_nav_history.csv")
    return df


def clean_aum_by_fund_house() -> pd.DataFrame:
    """Clean 03_aum_by_fund_house.csv: parse dates, validate numerics."""
    df = _load("03_aum_by_fund_house.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["aum_lakh_crore", "aum_crore", "num_schemes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["fund_house"] = df["fund_house"].astype(str).str.strip()
    df.drop_duplicates(subset=["date", "fund_house"], inplace=True)
    df.sort_values(["date", "fund_house"], inplace=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    _save(df, "03_aum_by_fund_house.csv")
    return df


def clean_monthly_sip_inflows() -> pd.DataFrame:
    """Clean 04_monthly_sip_inflows.csv: parse month, validate numerics."""
    df = _load("04_monthly_sip_inflows.csv")
    df["month"] = df["month"].astype(str).str.strip()
    for col in ["sip_inflow_crore", "active_sip_accounts_crore",
                 "new_sip_accounts_lakh", "sip_aum_lakh_crore", "yoy_growth_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.drop_duplicates(subset=["month"], inplace=True)
    df.sort_values("month", inplace=True)
    _save(df, "04_monthly_sip_inflows.csv")
    return df


def clean_category_inflows() -> pd.DataFrame:
    """Clean 05_category_inflows.csv."""
    df = _load("05_category_inflows.csv")
    df["month"] = df["month"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["net_inflow_crore"] = pd.to_numeric(df["net_inflow_crore"], errors="coerce")
    df.drop_duplicates(subset=["month", "category"], inplace=True)
    df.sort_values(["month", "category"], inplace=True)
    _save(df, "05_category_inflows.csv")
    return df


def clean_industry_folio_count() -> pd.DataFrame:
    """Clean 06_industry_folio_count.csv."""
    df = _load("06_industry_folio_count.csv")
    df["month"] = df["month"].astype(str).str.strip()
    for col in df.columns:
        if col != "month":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df.drop_duplicates(subset=["month"], inplace=True)
    df.sort_values("month", inplace=True)
    _save(df, "06_industry_folio_count.csv")
    return df


def clean_scheme_performance() -> pd.DataFrame:
    """Clean 07_scheme_performance.csv:
    - validate returns are numeric
    - flag negative Sharpe
    - check expense_ratio range
    """
    df = _load("07_scheme_performance.csv")
    numeric_cols = [
        "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
        "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
        "aum_crore", "expense_ratio_pct", "morningstar_rating",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    neg_sharpe = df[df["sharpe_ratio"] < 0]
    if len(neg_sharpe):
        print(f"    [WARN] {len(neg_sharpe)} schemes with negative Sharpe ratio")
    bad_er = df[(df["expense_ratio_pct"] < 0) | (df["expense_ratio_pct"] > 3.0)]
    if len(bad_er):
        print(f"    [WARN] {len(bad_er)} schemes with expense ratio outside 0-3%")
    for col in ["scheme_name", "fund_house", "category", "plan", "risk_grade"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df.drop_duplicates(subset=["amfi_code"], inplace=True)
    _save(df, "07_scheme_performance.csv")
    return df


def clean_investor_transactions() -> pd.DataFrame:
    """Clean 08_investor_transactions.csv:
    - standardise transaction_type (SIP / Lumpsum / Redemption)
    - validate amount > 0
    - check KYC values
    - fix date formats
    """
    df = _load("08_investor_transactions.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df = df[df["amount_inr"] > 0].copy()
    type_map = {
        "sip": "SIP", "SIP": "SIP",
        "lumpsum": "Lumpsum", "Lumpsum": "Lumpsum", "LUMPSUM": "Lumpsum",
        "redemption": "Redemption", "Redemption": "Redemption", "REDEMPTION": "Redemption",
    }
    df["transaction_type"] = (
        df["transaction_type"].astype(str).str.strip().map(type_map)
        .fillna(df["transaction_type"].str.strip())
    )
    valid_kyc = {"Verified", "Pending", "Rejected"}
    df["kyc_status"] = df["kyc_status"].astype(str).str.strip()
    bad_kyc = df[~df["kyc_status"].isin(valid_kyc)]
    if len(bad_kyc):
        print(f"    [WARN] {len(bad_kyc)} rows with unexpected KYC status")
    for col in ["investor_id", "state", "city", "city_tier",
                 "age_group", "gender", "payment_mode"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df["annual_income_lakh"] = pd.to_numeric(df["annual_income_lakh"], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.sort_values(["transaction_date", "investor_id"], inplace=True)
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    _save(df, "08_investor_transactions.csv")
    return df


def clean_portfolio_holdings() -> pd.DataFrame:
    """Clean 09_portfolio_holdings.csv: validate numerics, parse dates."""
    df = _load("09_portfolio_holdings.csv")
    df["portfolio_date"] = pd.to_datetime(df["portfolio_date"], errors="coerce")
    for col in ["weight_pct", "market_value_cr", "current_price_inr"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["stock_symbol", "stock_name", "sector"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df.drop_duplicates(subset=["amfi_code", "stock_symbol", "portfolio_date"], inplace=True)
    df["portfolio_date"] = df["portfolio_date"].dt.strftime("%Y-%m-%d")
    _save(df, "09_portfolio_holdings.csv")
    return df


def clean_benchmark_indices() -> pd.DataFrame:
    """Clean 10_benchmark_indices.csv: parse dates, validate numerics."""
    df = _load("10_benchmark_indices.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    df["close_value"] = pd.to_numeric(df["close_value"], errors="coerce")
    df["index_name"] = df["index_name"].astype(str).str.strip()
    df.drop_duplicates(subset=["date", "index_name"], inplace=True)
    df.sort_values(["index_name", "date"], inplace=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    _save(df, "10_benchmark_indices.csv")
    return df


# -- Master runner ---------------------------------------------------------

CLEANERS = [
    ("Fund Master",            clean_fund_master),
    ("NAV History",            clean_nav_history),
    ("AUM by Fund House",      clean_aum_by_fund_house),
    ("Monthly SIP Inflows",    clean_monthly_sip_inflows),
    ("Category Inflows",       clean_category_inflows),
    ("Industry Folio Count",   clean_industry_folio_count),
    ("Scheme Performance",     clean_scheme_performance),
    ("Investor Transactions",  clean_investor_transactions),
    ("Portfolio Holdings",     clean_portfolio_holdings),
    ("Benchmark Indices",      clean_benchmark_indices),
]


def run_cleaning() -> None:
    """Execute all cleaners and save processed CSVs."""
    print("\n" + "="*72)
    print("       BLUESTOCK MF -- DATA CLEANING")
    print("="*72 + "\n")

    for label, fn in CLEANERS:
        print(f"  > Cleaning {label} ...")
        try:
            fn()
        except Exception as e:
            print(f"    [ERR]  Error cleaning {label}: {e}")

    print(f"\n  [OK]  All datasets cleaned -> {PROCESSED_DIR}\n")


if __name__ == "__main__":
    run_cleaning()
