# Bluestock Fintech — Mutual Fund Analytics Platform

## Capstone Project | End-to-End Data Engineering, Financial Analytics & Interactive Streamlit Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

# 📋 Project Overview

The **Mutual Fund Analytics Platform** is a complete end-to-end Data Engineering and Analytics solution developed during the Bluestock Fintech Data Analyst Internship.

The project ingests publicly available mutual fund industry data, performs data cleaning and transformation through an ETL pipeline, stores processed data in a SQLite database, computes advanced financial metrics, and presents actionable insights through an interactive Streamlit dashboard.

The platform enables analysis of:

- Mutual Fund NAV performance
- Asset Under Management (AUM) growth
- SIP inflow trends
- Investor behavior and demographics
- Fund risk-return characteristics
- Benchmark comparisons
- Portfolio diversification
- Data quality monitoring

---

# 🚀 Key Features

### Data Engineering
- Automated ETL Pipeline
- Data Validation & Cleaning
- SQLite Database Integration
- Incremental Data Processing

### Analytics
- Exploratory Data Analysis (15+ Charts)
- Fund Performance Scorecards
- Sharpe Ratio Analysis
- Sortino Ratio Analysis
- Alpha & Beta Calculation
- CAGR Computation
- Value at Risk (VaR)
- Correlation Analysis

### Dashboard
- Interactive Streamlit Dashboard
- Multi-page Navigation
- Dynamic Filters
- KPI Cards
- Risk Analytics
- Automated Insights
- Data Quality Monitoring

### Advanced Features
- Fund Recommendation Engine
- Benchmark Comparison
- Rolling Performance Analytics
- Portfolio Holdings Analysis
- Investor Segmentation

---

# 🗂️ Project Structure

```text
bluestock_mf_capstone/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│       └── bluestock_mf.db
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   ├── 05_advanced_analytics.ipynb
│   └── EDA_Findings.md
│
├── scripts/
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── eda_analysis.py
│   ├── compute_metrics.py
│   ├── advanced_analytics.py
│   └── recommender.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
│   ├── app.py
│   └── logo_real.png
│
├── charts/
│   └── Analytical Visualizations
│
├── reports/
│   ├── Dashboard_Report.pdf
│   ├── Bluestock_MF_Analytics.pptx
│   └── Dashboard Screenshots
│
├── run_pipeline.py
├── requirements.txt
└── README.md
```

---

# 📊 Dataset Summary

| Dataset | Description |
|----------|------------|
| fund_master.csv | Master list of mutual fund schemes |
| nav_history.csv | Historical daily NAV values |
| aum_by_fund_house.csv | Quarterly AUM by AMC |
| monthly_sip_inflows.csv | Monthly SIP contributions |
| category_inflows.csv | Category-wise net inflows |
| industry_folio_count.csv | Industry folio growth |
| scheme_performance.csv | Risk-return metrics |
| investor_transactions.csv | Investor transaction data |
| portfolio_holdings.csv | Portfolio allocation details |
| benchmark_indices.csv | Market benchmark data |

Total Data Processed: **87,000+ records**

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/bluestock_mf_capstone.git
cd bluestock_mf_capstone
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Run Complete Pipeline

```bash
python run_pipeline.py
```

This executes:

1. Data Ingestion
2. Data Cleaning
3. Database Loading
4. Performance Analytics
5. EDA Generation
6. Advanced Analytics
7. Dashboard Data Preparation

---

## Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard will open automatically in your browser.

---

# 📈 Dashboard Modules

## 🏢 Industry Overview

- Total Industry AUM
- AMC Market Share
- SIP Growth Trends
- Category Inflows

---

## 📊 Fund Performance

- CAGR
- Alpha
- Beta
- Sharpe Ratio
- Sortino Ratio
- Risk-Return Analysis
- Fund Ranking Scorecard

---

## 👥 Investor Analytics

- State-wise Distribution
- Age Group Analysis
- Gender Distribution
- SIP vs Lumpsum Participation

---

## 📈 SIP & Market Trends

- SIP Growth Tracking
- Nifty Benchmark Comparison
- Market Correlation Analysis
- Category Heatmaps

---

## 🛡️ Risk Analytics

- Value at Risk (VaR)
- Volatility Analysis
- Drawdown Analysis
- Correlation Matrix

---

## 📋 Data Quality Monitor

- Missing Values
- Duplicate Detection
- Table Health Checks
- Dataset Validation Metrics

---

# 📌 Financial Metrics Implemented

### Return Metrics

- CAGR
- Annual Return
- Rolling Return

### Risk Metrics

- Standard Deviation
- Beta
- Maximum Drawdown
- Value at Risk (VaR)

### Risk-Adjusted Metrics

- Sharpe Ratio
- Sortino Ratio
- Alpha

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming | Python 3.10 |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Analytics | SciPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Version Control | Git, GitHub |
| Data Source | AMFI India, mfapi.in |

---

# 📄 Project Deliverables

| Deliverable | Status |
|-------------|---------|
| ETL Pipeline | ✅ Completed |
| Data Cleaning | ✅ Completed |
| SQLite Database | ✅ Completed |
| EDA Analysis | ✅ Completed |
| Performance Analytics | ✅ Completed |
| Advanced Analytics | ✅ Completed |
| Interactive Dashboard | ✅ Completed |
| Final Report | ✅ Completed |
| Presentation Deck | ✅ Completed |

---

# 🎯 Business Impact

This project demonstrates:

- Data Engineering Pipeline Design
- Financial Data Analysis
- Database Management
- Statistical Modeling
- Dashboard Development
- Business Intelligence Reporting
- End-to-End Analytics Workflow

---

# ⚠️ Disclaimer

This project is developed for educational and analytical purposes only.

Data has been sourced from publicly available mutual fund and financial market resources. The analysis presented should not be considered investment advice.

Mutual Fund investments are subject to market risks. Please read all scheme-related documents carefully before investing.

---

# 👨‍💻 Author

**Pratik Kumar Yadav**  
Data Analyst Intern — Bluestock Fintech

### Skills Demonstrated

- Python
- SQL
- SQLite
- Pandas
- NumPy
- Streamlit
- Data Visualization
- Financial Analytics
- ETL Pipelines
- Business Intelligence

---

⭐ If you found this project useful, consider giving it a star on GitHub.