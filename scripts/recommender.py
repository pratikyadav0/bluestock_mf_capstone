"""
recommender.py — Fund Recommendation Engine
Recommends top 3 funds based on investor risk appetite.
Bluestock Fintech Capstone Project
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'


def get_recommendations(risk_appetite: str) -> pd.DataFrame:
    """
    Recommend top 3 funds matching investor risk appetite.

    Args:
        risk_appetite: One of 'Low', 'Moderate', 'High', 'Very High'

    Returns:
        DataFrame with top 3 recommended funds
    """
    fm = pd.read_csv(RAW / '01_fund_master.csv')
    perf = pd.read_csv(RAW / '07_scheme_performance.csv')
    fm['amfi_code'] = fm['amfi_code'].astype(str)
    perf['amfi_code'] = perf['amfi_code'].astype(str)

    # Merge to get risk_category with performance
    merged = perf.merge(fm[['amfi_code', 'risk_category', 'plan', 'min_sip_amount']], on='amfi_code', how='left')

    # Filter by risk appetite
    risk_map = {
        'Low': ['Low', 'Moderate'],
        'Moderate': ['Moderate'],
        'High': ['High', 'Very High'],
        'Very High': ['Very High']
    }
    allowed = risk_map.get(risk_appetite, [risk_appetite])
    filtered = merged[merged['risk_category'].isin(allowed)]

    if filtered.empty:
        print(f"  No funds found for risk appetite: {risk_appetite}")
        return pd.DataFrame()

    # Sort by Sharpe Ratio (best risk-adjusted returns)
    top3 = filtered.nlargest(3, 'sharpe_ratio')

    display_cols = ['scheme_name', 'category', 'plan', 'risk_category',
                    'return_1yr_pct', 'return_3yr_pct', 'sharpe_ratio',
                    'sortino_ratio', 'alpha', 'max_drawdown_pct',
                    'expense_ratio_pct', 'morningstar_rating', 'min_sip_amount']
    display_cols = [c for c in display_cols if c in top3.columns]
    return top3[display_cols].reset_index(drop=True)


def print_recommendation(risk_appetite: str):
    """Print formatted recommendation table."""
    print(f"\n{'='*70}")
    print(f"  FUND RECOMMENDATIONS — Risk Appetite: {risk_appetite.upper()}")
    print(f"{'='*70}")

    recs = get_recommendations(risk_appetite)
    if recs.empty:
        print("  No matching funds found.\n")
        return

    for i, (_, row) in enumerate(recs.iterrows(), 1):
        name = str(row.get('scheme_name', ''))
        short = name.replace(' - Growth', '')[:50]
        stars_str = '*' * int(row.get('morningstar_rating', 0))
        print(f"\n  #{i} {short}")
        print(f"      Category:     {row.get('category', '—')} ({row.get('plan', '—')})")
        print(f"      Risk Grade:   {row.get('risk_category', '—')}")
        print(f"      1Y Return:    {row.get('return_1yr_pct', 0):+.2f}%")
        print(f"      3Y CAGR:      {row.get('return_3yr_pct', 0):+.2f}%")
        print(f"      Sharpe Ratio: {row.get('sharpe_ratio', 0):.2f}")
        print(f"      Sortino:      {row.get('sortino_ratio', 0):.2f}")
        print(f"      Alpha:        {row.get('alpha', 0):+.2f}%")
        print(f"      Max Drawdown: {row.get('max_drawdown_pct', 0):.2f}%")
        print(f"      Expense Ratio:{row.get('expense_ratio_pct', 0):.2f}%")
        print(f"      Rating:       {stars_str or '—'}")
        print(f"      Min SIP:      Rs. {int(row.get('min_sip_amount', 500)):,}")


def main():
    print("=" * 60)
    print("MUTUAL FUND RECOMMENDATION ENGINE")
    print("Bluestock Fintech")
    print("=" * 60)
    print("\nThis tool recommends the top 3 funds based on your risk appetite.")
    print("Risk categories: Low, Moderate, High, Very High\n")

    # Demo: show recommendations for all risk levels
    for risk in ['Low', 'Moderate', 'High', 'Very High']:
        print_recommendation(risk)

    print(f"\n{'='*70}")
    print("  DISCLAIMER: This is for educational purposes only.")
    print("  Mutual Fund investments are subject to market risks.")
    print("  Read all scheme-related documents carefully before investing.")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
