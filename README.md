# Bluestock Fintech — Mutual Fund Analytics Platform

## Capstone Project | End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Chart.js](https://img.shields.io/badge/Dashboard-Chart.js-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📋 Project Overview

A full-stack **Mutual Fund Analytics Platform** that ingests publicly available data from AMFI India, transforms it through a robust ETL pipeline, stores it in a relational database, and presents insights via an interactive dashboard.

**Key Features:**
- 📊 Tracks NAV movements of 40+ mutual fund schemes from top AMCs
- 📈 Monitors AUM growth trends for 10 largest fund houses over 4+ years
- 👥 Analyses investor behaviour patterns across geographies & demographics
- ⚡ Computes risk-adjusted return metrics (Sharpe, Sortino, Alpha, Beta)
- 🎯 Benchmarks fund performance against Nifty 50, Nifty 100, BSE SmallCap
- 🖥️ Interactive 4-page web dashboard with real-time filtering

---

## 🗂️ Project Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/                ← 10 original CSV datasets (87K+ rows)
│   ├── processed/          ← Cleaned CSVs + computed metrics
│   └── db/                 ← bluestock_mf.db (SQLite database)
├── scripts/
│   ├── etl_pipeline.py     ← D1: Data ingestion & DB loading
│   ├── data_cleaning.py    ← D1: Data validation & cleaning
│   ├── live_nav_fetch.py   ← D1: Live NAV from mfapi.in
│   ├── eda_analysis.py     ← D3: 15+ EDA charts
│   ├── compute_metrics.py  ← D4: Performance metrics & scorecard
│   ├── advanced_analytics.py ← D6: VaR, Rolling Sharpe, Cohorts
│   ├── recommender.py      ← D6: Fund recommendation engine
│   └── generate_dashboard_data.py ← D5: Dashboard JSON generation
├── sql/
│   ├── schema.sql          ← D2: Star schema DDL
│   └── queries.sql         ← D2: 10 analytical SQL queries
├── dashboard/
│   ├── index.html          ← D5: Interactive dashboard
│   ├── style.css           ← D5: Dark glassmorphism theme
│   ├── app.js              ← D5: Chart.js visualisations
│   └── data/               ← JSON data for dashboard
├── charts/                 ← 15+ exported PNG charts
├── reports/
│   └── data_dictionary.md  ← D7: Complete schema reference
├── run_pipeline.py         ← Master pipeline script
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Complete Pipeline

```bash
python run_pipeline.py
```

This will:
1. Ingest all 10 CSV datasets
2. Clean and validate data
3. Load into SQLite database
4. Compute all performance metrics
5. Generate EDA charts
6. Run advanced analytics
7. Generate dashboard data

### 3. Open the Dashboard

#### Option A: Run the Streamlit Dashboard (Recommended)
This launches the premium, interactive Streamlit analytics platform featuring 7 pages, advanced risk analytics, data quality monitoring, and automated insights:

```bash
python -m streamlit run dashboard/app.py
```

#### Option B: Open Static Web Dashboard
Alternatively, you can open the static HTML/JS dashboard:

```bash
# Windows
start dashboard\index.html

# Mac
open dashboard/index.html
```

### 4. Run Individual Scripts

```bash
# ETL Pipeline only
python scripts/etl_pipeline.py

# EDA Analysis (generates 15+ charts)
python scripts/eda_analysis.py

# Performance Metrics
python scripts/compute_metrics.py

# Advanced Analytics (VaR, Cohorts, HHI)
python scripts/advanced_analytics.py

# Fund Recommender
python scripts/recommender.py

# Live NAV Fetch
python scripts/live_nav_fetch.py
```

---

## 📊 Dashboard Pages (Streamlit App)

| Page | Description |
|------|-------------|
| **🏆 Executive Dashboard** | High-level landing page. Displays total AUM, monthly SIP inflow, total schemes, top AMC, and best performer. Includes an automated insight engine. |
| **🌐 Industry Overview** | Visualizes historical SIP inflow trends, AUM split by AMC (Top 10), folio count growth, and category-wise monthly inflows. Filterable by Year. |
| **⚡ Fund Performance** | Dynamic risk-return metrics (CAGR, Alpha, Beta, Sharpe, Sortino). Features a risk-return scatter bubble chart, composite rankings, and a sortable, exportable scorecard table. Filterable by AMC, Category, and Risk. |
| **👥 Investor Analytics** | Tracks investor geographic distribution (by state), demographic splits (age groups, gender), investment type distribution (SIP vs. Lumpsum), and tier share. Filterable by State, Age, and Tier. |
| **📈 SIP & Market Trends** | Analyzes correlations between retail savings (SIP) and market index (Nifty 50) using dual y-axes. Includes normalized benchmark index line charts and a category inflow heatmap. Filterable by Year and Category. |
| **🛡️ Risk & Correlation** | Dedicated financial risk page displaying Value at Risk (VaR), Conditional VaR (CVaR), standard deviation vs drawdown, and correlation matrix between major benchmark indices. |
| **📋 Data Quality Monitor** | In-app data engineering audit panel. Shows table row counts, duplicate checks, null counts, date coverage, and automated system warning flags. |


---

## 📈 Datasets (10 CSV files, 87K+ rows)

| # | File | Rows | Description |
|---|------|------|-------------|
| 01 | fund_master.csv | 40 | Master list of 40 real MF schemes |
| 02 | nav_history.csv | ~46K | Daily NAV (Jan 2022 – May 2026) |
| 03 | aum_by_fund_house.csv | ~90 | Quarterly AUM for 10 fund houses |
| 04 | monthly_sip_inflows.csv | 48 | Monthly SIP data (AMFI) |
| 05 | category_inflows.csv | ~144 | Net inflows by category |
| 06 | industry_folio_count.csv | 21 | Folio growth milestones |
| 07 | scheme_performance.csv | 40 | Returns, Sharpe, Alpha, Beta |
| 08 | investor_transactions.csv | ~32K | 5,000 investor transactions |
| 09 | portfolio_holdings.csv | ~320 | Top equity holdings by fund |
| 10 | benchmark_indices.csv | ~8K | Daily index values |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| Database | SQLite3, SQLAlchemy |
| Visualisation | Matplotlib, Seaborn, Chart.js |
| Statistics | SciPy (OLS regression) |
| Dashboard | HTML5, CSS3, JavaScript |
| API | mfapi.in (live NAV) |

---

## 📄 Deliverables

| # | Deliverable | Weight | Format |
|---|------------|--------|--------|
| D1 | ETL Pipeline Script | 15% | Python .py |
| D2 | SQLite Database | 10% | .db file |
| D3 | EDA Notebook | 15% | Python script + 15 PNGs |
| D4 | Performance Metrics | 15% | Python + CSVs |
| D5 | Interactive Dashboard | 20% | HTML/CSS/JS |
| D6 | Advanced Analytics | 10% | Python + CSVs |
| D7 | Final Report + README | 15% | Markdown + PDF |

---

## ⚠️ Disclaimer

All data is sourced from publicly available AMFI India data, mfapi.in, and financial news sources. This project is for **educational purposes only** and does not constitute financial advice. Mutual Fund investments are subject to market risks.

---

**Prepared by:** Pratik Kumar Yadav — Data Analyst Intern, Bluestock Fintech  
**Date:** June 2026  
**Company:** Bluestock Fintech Pvt. Ltd.
