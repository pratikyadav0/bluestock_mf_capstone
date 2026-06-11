# Data Dictionary — Bluestock MF Capstone

Complete schema reference for all 10 datasets used in the Mutual Fund Analytics Platform.

---

## 01_fund_master.csv (40 rows)
Master list of 40 real mutual fund schemes.

| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | AMFI unique scheme code (PK). e.g. 125497 = HDFC Top 100 Direct |
| fund_house | TEXT | AMC name (e.g. SBI Mutual Fund, HDFC Mutual Fund) |
| scheme_name | TEXT | Full official AMFI scheme name |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap / Liquid / etc. |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund launch date (YYYY-MM-DD) |
| benchmark | TEXT | Official benchmark index (e.g. NIFTY 100 TRI) |
| expense_ratio_pct | REAL | Annual expense ratio in % (e.g. 1.05) |
| exit_load_pct | REAL | Exit load % (0 for Liquid/Index funds) |
| min_sip_amount | INT | Minimum SIP amount in INR |
| min_lumpsum_amount | INT | Minimum lumpsum investment in INR |
| fund_manager | TEXT | Name of primary fund manager |
| risk_category | TEXT | SEBI risk: Low / Moderate / High / Very High |
| sebi_category_code | TEXT | Internal code: EC01=LargeCap, EC03=SmallCap, DC01=Liquid |

---

## 02_nav_history.csv (~46,000 rows)
Daily NAV for all 40 schemes from Jan 2022 to May 2026.

| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | FK to fund_master |
| date | DATE | NAV date (business days only, YYYY-MM-DD) |
| nav | REAL | Net Asset Value in Rs. (e.g. 892.4560) |

---

## 03_aum_by_fund_house.csv (~90 rows)
Quarterly AUM for 10 fund houses (2022–2025).

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Quarter end date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | AUM in Rs. Lakh Crore |
| aum_crore | REAL | AUM in Rs. Crore |
| num_schemes | INT | Number of schemes managed |

---

## 04_monthly_sip_inflows.csv (48 rows)
Monthly SIP data from AMFI Monthly Notes (Jan 2022–Dec 2025).

| Column | Type | Description |
|--------|------|-------------|
| month | TEXT | YYYY-MM format |
| sip_inflow_crore | REAL | Total SIP inflows in Rs. Crore |
| active_sip_accounts_crore | REAL | Active SIP accounts in Crore |
| new_sip_accounts_lakh | REAL | New SIP registrations in Lakh |
| sip_aum_lakh_crore | REAL | SIP AUM in Rs. Lakh Crore |
| yoy_growth_pct | REAL | Year-over-Year growth % |

---

## 05_category_inflows.csv (~144 rows)
Net inflows by fund category for FY 2024-25.

| Column | Type | Description |
|--------|------|-------------|
| month | TEXT | YYYY-MM format |
| category | TEXT | Fund category (Large Cap, Mid Cap, etc.) |
| net_inflow_crore | REAL | Net inflow in Rs. Crore |

---

## 06_industry_folio_count.csv (21 rows)
Total mutual fund folios broken by type.

| Column | Type | Description |
|--------|------|-------------|
| month | TEXT | YYYY-MM format |
| total_folios_crore | REAL | Total MF folios in Crore |
| equity_folios_crore | REAL | Equity folios in Crore |
| debt_folios_crore | REAL | Debt folios in Crore |
| hybrid_folios_crore | REAL | Hybrid folios in Crore |
| others_folios_crore | REAL | Others folios in Crore |

---

## 07_scheme_performance.csv (40 rows)
Pre-computed performance metrics for all 40 schemes.

| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | FK to fund_master |
| scheme_name | TEXT | Scheme name |
| fund_house | TEXT | AMC name |
| category | TEXT | Equity / Debt / Hybrid |
| plan | TEXT | Regular / Direct |
| return_1yr_pct | REAL | 1-year absolute return % |
| return_3yr_pct | REAL | 3-year CAGR % |
| return_5yr_pct | REAL | 5-year CAGR % |
| benchmark_3yr_pct | REAL | Benchmark index 3yr CAGR |
| alpha | REAL | Return above benchmark |
| beta | REAL | Market sensitivity (1.0 = same as market) |
| sharpe_ratio | REAL | Risk-adjusted return (>1 is good) |
| sortino_ratio | REAL | Like Sharpe but penalises only downside |
| std_dev_ann_pct | REAL | Annualised standard deviation % |
| max_drawdown_pct | REAL | Worst peak-to-trough decline (negative) |
| aum_crore | REAL | Fund AUM in Crore |
| expense_ratio_pct | REAL | Expense ratio % |
| morningstar_rating | INT | 1-5 star rating |
| risk_grade | TEXT | Low / Moderate / High / Very High |

---

## 08_investor_transactions.csv (~32,000 rows)
Simulated transactions for 5,000 investors.

| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique ID (INV000001–INV005000) |
| transaction_date | DATE | Date of transaction |
| amfi_code | TEXT | FK to fund_master |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INT | Amount in Indian Rupees |
| state | TEXT | Investor's state (12 states) |
| city | TEXT | Investor's city |
| city_tier | TEXT | T30 (Top 30) or B30 (Beyond 30) |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| gender | TEXT | Male / Female |
| annual_income_lakh | REAL | Annual income in Rs. Lakh |
| payment_mode | TEXT | UPI / Net Banking / Mandate / Cheque |
| kyc_status | TEXT | Verified (92%) / Pending (8%) |

---

## 09_portfolio_holdings.csv (~320 rows)
Top equity holdings per fund as of Dec 2025.

| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | FK to fund_master |
| stock_symbol | TEXT | NSE stock symbol |
| stock_name | TEXT | Company name |
| sector | TEXT | Industry sector |
| weight_pct | REAL | Portfolio weight % |
| market_value_cr | REAL | Market value in Crore |
| current_price_inr | REAL | Current stock price |
| portfolio_date | DATE | Holdings as-of date |

---

## 10_benchmark_indices.csv (~8,000 rows)
Daily closing values for benchmark indices.

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Trading date |
| index_name | TEXT | Nifty 50 / Nifty 100 / Nifty Midcap 150 / BSE SmallCap / CRISIL Liquid / CRISIL Gilt |
| close_value | REAL | Daily closing value |

---

## Derived Tables (SQLite Database)

### dim_date
| Column | Type | Description |
|--------|------|-------------|
| date_id | TEXT PK | Date in YYYY-MM-DD format |
| date | DATE | Date value |
| year | INT | Year |
| month | INT | Month (1-12) |
| quarter | INT | Quarter (1-4) |
| day_of_week | INT | Day of week (0=Mon) |
| is_weekday | BOOLEAN | True if Mon-Fri |

### Computed Outputs
| File | Description |
|------|-------------|
| returns_computed.csv | Daily returns for all funds |
| cagr_report.csv | 1yr/3yr/5yr CAGR per fund |
| alpha_beta.csv | Alpha and Beta vs benchmark |
| fund_scorecard.csv | Composite fund score (0-100) |
| var_cvar_report.csv | Value at Risk (95%) and CVaR |
| cohort_analysis.csv | Investor cohort metrics |
| sip_continuity.csv | SIP gap analysis |
| sector_hhi.csv | Sector concentration index |
