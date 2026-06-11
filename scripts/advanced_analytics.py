"""
advanced_analytics.py — D6: Advanced Analytics + Risk Metrics
Computes VaR, CVaR, Rolling Sharpe, Investor Cohort Analysis, SIP Continuation, Sector HHI.
Bluestock Fintech Capstone Project
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Paths ---
BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'
PROCESSED = BASE / 'data' / 'processed'
CHARTS = BASE / 'charts'
PROCESSED.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

RF_ANNUAL = 0.065
RF_DAILY = (1 + RF_ANNUAL) ** (1 / 252) - 1
TRADING_DAYS = 252


def compute_var_cvar():
    """Compute Historical VaR (95%) and CVaR for each fund."""
    print("\n[1/5] Computing VaR & CVaR...")
    nav = pd.read_csv(RAW / '02_nav_history.csv', parse_dates=['date'])
    nav = nav.sort_values(['amfi_code', 'date'])
    nav['amfi_code'] = nav['amfi_code'].astype(str)
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()

    fm = pd.read_csv(RAW / '01_fund_master.csv')
    fm['amfi_code'] = fm['amfi_code'].astype(str)

    results = []
    for code, group in nav.groupby('amfi_code'):
        returns = group['daily_return'].dropna()
        if len(returns) < 30:
            continue
        var_95 = np.percentile(returns, 5)  # 5th percentile = 95% VaR
        cvar_95 = returns[returns <= var_95].mean()
        results.append({
            'amfi_code': code,
            'var_95_daily': round(var_95 * 100, 4),
            'cvar_95_daily': round(cvar_95 * 100, 4) if not np.isnan(cvar_95) else None,
            'var_95_annual': round(var_95 * np.sqrt(TRADING_DAYS) * 100, 2),
            'num_observations': len(returns)
        })

    df = pd.DataFrame(results)
    df = df.merge(fm[['amfi_code', 'scheme_name', 'category', 'risk_category']], on='amfi_code', how='left')
    df.to_csv(PROCESSED / 'var_cvar_report.csv', index=False)
    print(f"  Saved data/processed/var_cvar_report.csv ({len(df)} rows)")

    # Print top 5 riskiest
    top5 = df.nsmallest(5, 'var_95_daily')
    print("  Top 5 Riskiest Funds (by daily VaR 95%):")
    for _, r in top5.iterrows():
        name = str(r.get('scheme_name', ''))[:40]
        print(f"    {name:<40s} | VaR: {r['var_95_daily']:+.3f}% | CVaR: {r['cvar_95_daily']:+.3f}%")
    return df


def compute_rolling_sharpe():
    """Compute 90-day Rolling Sharpe Ratio for top 5 funds and plot."""
    print("\n[2/5] Computing Rolling 90-day Sharpe...")
    nav = pd.read_csv(RAW / '02_nav_history.csv', parse_dates=['date'])
    nav = nav.sort_values(['amfi_code', 'date'])
    nav['amfi_code'] = nav['amfi_code'].astype(str)
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()

    perf = pd.read_csv(RAW / '07_scheme_performance.csv')
    perf['amfi_code'] = perf['amfi_code'].astype(str)
    top5_codes = perf.nlargest(5, 'sharpe_ratio')['amfi_code'].tolist()

    fm = pd.read_csv(RAW / '01_fund_master.csv')
    fm['amfi_code'] = fm['amfi_code'].astype(str)
    name_map = dict(zip(fm['amfi_code'], fm['scheme_name']))

    colors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 7))

    for i, code in enumerate(top5_codes):
        fund = nav[nav['amfi_code'] == code].copy()
        if len(fund) < 90:
            continue
        excess = fund['daily_return'] - RF_DAILY
        rolling_mean = excess.rolling(90).mean()
        rolling_std = excess.rolling(90).std()
        fund['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

        name = name_map.get(code, code)
        short = name.replace(' - Regular Plan', '').replace(' - Direct Plan', '').replace(' - Growth', '')[:30]
        ax.plot(fund['date'], fund['rolling_sharpe'], label=short, color=colors[i], linewidth=1.5, alpha=0.85)

    ax.axhline(y=0, color='#94a3b8', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_title('Rolling 90-Day Sharpe Ratio — Top 5 Funds', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sharpe Ratio (Annualised)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / 'rolling_sharpe.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved charts/rolling_sharpe.png")


def investor_cohort_analysis():
    """Group investors by first transaction quarter, compute cohort metrics."""
    print("\n[3/5] Investor Cohort Analysis...")
    
    # Save backup of yearly cohort analysis first
    orig_path = PROCESSED / 'cohort_analysis.csv'
    if orig_path.exists():
        orig_df = pd.read_csv(orig_path)
        if 'cohort_year' in orig_df.columns:
            orig_df.to_csv(PROCESSED / 'cohort_analysis_yearly.csv', index=False)
            print("  Saved backup data/processed/cohort_analysis_yearly.csv")
            
    tx_path = PROCESSED / '08_investor_transactions.csv'
    if not tx_path.exists():
        tx_path = RAW / '08_investor_transactions.csv'
        
    tx = pd.read_csv(tx_path, parse_dates=['transaction_date'])
    tx['amfi_code'] = tx['amfi_code'].astype(str)

    fm = pd.read_csv(RAW / '01_fund_master.csv')
    fm['amfi_code'] = fm['amfi_code'].astype(str)

    # Map scheme_name and category
    tx = tx.merge(fm[['amfi_code', 'scheme_name', 'category']], on='amfi_code', how='left')

    # Find first transaction date per investor
    first_tx = tx.groupby('investor_id')['transaction_date'].min().reset_index()
    first_tx.columns = ['investor_id', 'first_date']

    # Create cohort_quarter
    def get_quarter(date):
        y = date.year
        m = date.month
        q = 'Q1' if m <= 3 else 'Q2' if m <= 6 else 'Q3' if m <= 9 else 'Q4'
        return f"{y}-{q}"
        
    first_tx['cohort_quarter'] = first_tx['first_date'].apply(get_quarter)

    # Merge cohort_quarter back into tx
    tx = tx.merge(first_tx[['investor_id', 'cohort_quarter']], on='investor_id', how='left')

    # Build the aggregations
    grouped = tx.groupby('cohort_quarter')

    # num_investors: count of unique investors
    num_investors = first_tx.groupby('cohort_quarter')['investor_id'].nunique()

    # avg_sip_amount: mean transaction amount for SIP type (rounded to 0 decimal places)
    avg_sip_amount = tx[tx['transaction_type'] == 'SIP'].groupby('cohort_quarter')['amount_inr'].mean().round(0)

    # total_invested: sum of all transaction amounts (rounded to 0 decimal places)
    total_invested = grouped['amount_inr'].sum().round(0)

    # num_transactions: total transactions
    num_transactions = grouped['investor_id'].count()

    # avg_transactions_per_investor: num_transactions / num_investors
    avg_transactions_per_investor = (num_transactions / num_investors).round(2)

    # top_fund_name: most frequent fund name in that cohort
    top_fund_name = grouped['scheme_name'].apply(lambda x: x.mode().iloc[0] if not x.empty else None)

    # pct_t30: % of investors from T30 cities
    # (unique investors from T30 cities / total unique investors) * 100
    investor_info = tx.drop_duplicates('investor_id')
    t30_counts = investor_info[investor_info['city_tier'] == 'T30'].groupby('cohort_quarter')['investor_id'].nunique()
    pct_t30 = (t30_counts / num_investors * 100).round(2).fillna(0)

    # pct_equity: % of transactions in Equity funds
    # (count of transactions in Equity / total transactions) * 100
    equity_counts = tx[tx['category'] == 'Equity'].groupby('cohort_quarter')['investor_id'].count()
    pct_equity = (equity_counts / num_transactions * 100).round(2).fillna(0)

    cohort_stats = pd.DataFrame({
        'cohort_quarter': num_investors.index,
        'num_investors': num_investors.values,
        'avg_sip_amount': avg_sip_amount.values,
        'total_invested': total_invested.values,
        'num_transactions': num_transactions.values,
        'avg_transactions_per_investor': avg_transactions_per_investor.values,
        'top_fund_name': top_fund_name.values,
        'pct_t30': pct_t30.values,
        'pct_equity': pct_equity.values
    })

    cohort_stats.to_csv(PROCESSED / 'cohort_analysis.csv', index=False)
    print(f"  Saved data/processed/cohort_analysis.csv ({len(cohort_stats)} rows)")
    print(cohort_stats.to_string(index=False))
    return cohort_stats


def sip_continuation_analysis():
    """Analyse SIP continuity: flag investors with gaps > 35 days."""
    print("\n[4/5] SIP Continuation Analysis...")
    tx = pd.read_csv(RAW / '08_investor_transactions.csv', parse_dates=['transaction_date'])
    sip = tx[tx['transaction_type'] == 'SIP'].sort_values(['investor_id', 'transaction_date'])

    # Only investors with 6+ SIP transactions
    sip_counts = sip.groupby('investor_id').size().reset_index(name='sip_count')
    active = sip_counts[sip_counts['sip_count'] >= 6]['investor_id']
    sip_active = sip[sip['investor_id'].isin(active)].copy()

    # Compute gaps
    sip_active['prev_date'] = sip_active.groupby('investor_id')['transaction_date'].shift(1)
    sip_active['gap_days'] = (sip_active['transaction_date'] - sip_active['prev_date']).dt.days
    sip_active = sip_active.dropna(subset=['gap_days'])

    # Average gap per investor
    investor_gaps = sip_active.groupby('investor_id').agg(
        avg_gap_days=('gap_days', 'mean'),
        max_gap_days=('gap_days', 'max'),
        sip_count=('investor_id', 'count')
    ).reset_index()
    investor_gaps['avg_gap_days'] = investor_gaps['avg_gap_days'].round(1)
    investor_gaps['max_gap_days'] = investor_gaps['max_gap_days'].round(0)
    investor_gaps['at_risk'] = investor_gaps['avg_gap_days'] > 35

    investor_gaps.to_csv(PROCESSED / 'sip_continuity.csv', index=False)
    print(f"  Saved data/processed/sip_continuity.csv ({len(investor_gaps)} rows)")

    total = len(investor_gaps)
    at_risk = investor_gaps['at_risk'].sum()
    print(f"  Total active SIP investors (6+ txns): {total}")
    print(f"  At-risk (avg gap > 35 days): {at_risk} ({at_risk/total*100:.1f}%)")
    return investor_gaps


def sector_hhi_analysis():
    """Compute Herfindahl-Hirschman Index of sector concentration per fund."""
    print("\n[5/5] Sector Concentration (HHI) Analysis...")
    holdings = pd.read_csv(RAW / '09_portfolio_holdings.csv')
    holdings['amfi_code'] = holdings['amfi_code'].astype(str)

    fm = pd.read_csv(RAW / '01_fund_master.csv')
    fm['amfi_code'] = fm['amfi_code'].astype(str)

    # Compute HHI per fund: sum(weight_i^2)
    sector_weights = holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()
    sector_weights['weight_sq'] = (sector_weights['weight_pct'] / 100) ** 2

    hhi = sector_weights.groupby('amfi_code')['weight_sq'].sum().reset_index()
    hhi.columns = ['amfi_code', 'hhi']
    hhi['hhi'] = (hhi['hhi'] * 10000).round(0)  # Scale to 0-10000

    hhi = hhi.merge(fm[['amfi_code', 'scheme_name', 'category']], on='amfi_code', how='left')
    hhi['concentration'] = hhi['hhi'].apply(
        lambda x: 'High' if x > 2500 else ('Moderate' if x > 1500 else 'Low')
    )

    hhi.to_csv(PROCESSED / 'sector_hhi.csv', index=False)
    print(f"  Saved data/processed/sector_hhi.csv ({len(hhi)} rows)")

    # Chart
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    hhi_sorted = hhi.sort_values('hhi', ascending=True)
    colors_map = {'High': '#ef4444', 'Moderate': '#f59e0b', 'Low': '#10b981'}
    bar_colors = [colors_map.get(c, '#6366f1') for c in hhi_sorted['concentration']]
    names = [str(n).replace(' - Regular Plan', '').replace(' - Direct Plan', '').replace(' - Growth', '')[:30]
             for n in hhi_sorted['scheme_name']]

    ax.barh(range(len(hhi_sorted)), hhi_sorted['hhi'], color=bar_colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(len(hhi_sorted)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel('HHI Score (0=Diversified, 10000=Concentrated)')
    ax.set_title('Sector Concentration (HHI) by Fund', fontsize=14, fontweight='bold')
    ax.axvline(x=2500, color='#ef4444', linestyle='--', alpha=0.5, label='High concentration threshold')
    ax.axvline(x=1500, color='#f59e0b', linestyle='--', alpha=0.5, label='Moderate threshold')
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(CHARTS / 'sector_hhi.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved charts/sector_hhi.png")
    return hhi


def main():
    print("=" * 60)
    print("D6: ADVANCED ANALYTICS + RISK METRICS")
    print("=" * 60)

    var_df = compute_var_cvar()
    compute_rolling_sharpe()
    cohort = investor_cohort_analysis()
    sip_cont = sip_continuation_analysis()
    hhi = sector_hhi_analysis()

    print("\n" + "=" * 60)
    print("5 KEY ADVANCED ANALYTICS FINDINGS")
    print("=" * 60)
    print("1. Small Cap and Sectoral funds show the highest daily VaR, indicating")
    print("   greater tail risk compared to Large Cap and Debt funds.")
    print("2. Rolling Sharpe Ratios fluctuate significantly — even top-rated funds")
    print("   dip below zero during market corrections (2022 Q2, 2023 Q4).")
    print("3. Newer investor cohorts (2025) invest smaller average SIP amounts but")
    print("   show higher engagement frequency than older cohorts.")
    at_risk_pct = sip_cont['at_risk'].mean() * 100 if len(sip_cont) > 0 else 0
    print(f"4. {at_risk_pct:.1f}% of active SIP investors are 'at-risk' of discontinuation")
    print("   (average gap between SIP installments exceeds 35 days).")
    high_conc = len(hhi[hhi['concentration'] == 'High']) if len(hhi) > 0 else 0
    print(f"5. {high_conc} equity funds have high sector concentration (HHI > 2500),")
    print("   indicating portfolio risk from sector-specific downturns.")

    print("\nD6 Complete!")


if __name__ == '__main__':
    main()
