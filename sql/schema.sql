-- ============================================================
-- Bluestock Mutual Fund Analytics — Star Schema
-- Database: SQLite (bluestock_mf.db)
-- ============================================================

-- ===================== DIMENSION TABLES =====================

-- Dimension: Fund Master
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT NOT NULL,
    scheme_name         TEXT NOT NULL,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      REAL,
    min_lumpsum_amount  REAL,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

-- Dimension: Date (generated programmatically 2022-01-01 to 2026-05-31)
CREATE TABLE IF NOT EXISTS dim_date (
    date_id     INTEGER PRIMARY KEY,   -- YYYYMMDD format
    date        TEXT NOT NULL UNIQUE,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    quarter     INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    is_weekday  INTEGER NOT NULL        -- 1 = weekday, 0 = weekend
);

-- ===================== FACT TABLES ===========================

-- Fact: Daily NAV
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code       INTEGER NOT NULL,
    nav_date        TEXT NOT NULL,
    nav             REAL NOT NULL,
    daily_return_pct REAL,
    PRIMARY KEY (amfi_code, nav_date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Investor Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    amfi_code           INTEGER NOT NULL,
    transaction_date    TEXT,
    transaction_type    TEXT,
    amount_inr          REAL,
    state               TEXT,
    city                TEXT,
    city_tier           TEXT,
    age_group           TEXT,
    gender              TEXT,
    annual_income_lakh  REAL,
    payment_mode        TEXT,
    kyc_status          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Scheme Performance (point-in-time snapshot)
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code           INTEGER PRIMARY KEY,
    scheme_name         TEXT,
    fund_house          TEXT,
    category            TEXT,
    plan                TEXT,
    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,
    benchmark_3yr_pct   REAL,
    alpha               REAL,
    beta                REAL,
    sharpe_ratio        REAL,
    sortino_ratio       REAL,
    std_dev_ann_pct     REAL,
    max_drawdown_pct    REAL,
    aum_crore           REAL,
    expense_ratio_pct   REAL,
    morningstar_rating  INTEGER,
    risk_grade          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Portfolio Holdings
CREATE TABLE IF NOT EXISTS fact_portfolio (
    amfi_code       INTEGER NOT NULL,
    stock_symbol    TEXT NOT NULL,
    stock_name      TEXT,
    sector          TEXT,
    weight_pct      REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date  TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: AUM by Fund House (quarterly)
CREATE TABLE IF NOT EXISTS fact_aum (
    fund_house      TEXT NOT NULL,
    date            TEXT NOT NULL,
    aum_lakh_crore  REAL,
    aum_crore       REAL,
    num_schemes     INTEGER,
    PRIMARY KEY (fund_house, date)
);

-- Fact: SIP Industry Aggregates (monthly)
CREATE TABLE IF NOT EXISTS fact_sip_industry (
    month                   TEXT PRIMARY KEY,
    sip_inflow_crore        REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh   REAL,
    sip_aum_lakh_crore      REAL,
    yoy_growth_pct          REAL
);

-- Supplementary: Category Inflows
CREATE TABLE IF NOT EXISTS fact_category_inflows (
    month           TEXT NOT NULL,
    category        TEXT NOT NULL,
    net_inflow_crore REAL,
    PRIMARY KEY (month, category)
);

-- Supplementary: Industry Folio Count
CREATE TABLE IF NOT EXISTS fact_folio_count (
    month                TEXT PRIMARY KEY,
    total_folios_crore   REAL,
    equity_folios_crore  REAL,
    debt_folios_crore    REAL,
    hybrid_folios_crore  REAL,
    others_folios_crore  REAL
);

-- Supplementary: Benchmark Indices
CREATE TABLE IF NOT EXISTS fact_benchmark_indices (
    date        TEXT NOT NULL,
    index_name  TEXT NOT NULL,
    close_value REAL,
    PRIMARY KEY (date, index_name)
);

-- ===================== INDEXES ===============================

CREATE INDEX IF NOT EXISTS idx_fact_nav_amfi       ON fact_nav(amfi_code);
CREATE INDEX IF NOT EXISTS idx_fact_nav_date       ON fact_nav(nav_date);
CREATE INDEX IF NOT EXISTS idx_fact_tx_amfi        ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_fact_tx_date        ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_fact_tx_investor    ON fact_transactions(investor_id);
CREATE INDEX IF NOT EXISTS idx_fact_perf_cat       ON fact_performance(category);
CREATE INDEX IF NOT EXISTS idx_fact_port_amfi      ON fact_portfolio(amfi_code);
CREATE INDEX IF NOT EXISTS idx_fact_aum_date       ON fact_aum(date);
CREATE INDEX IF NOT EXISTS idx_fact_bench_date     ON fact_benchmark_indices(date);
CREATE INDEX IF NOT EXISTS idx_dim_date_date       ON dim_date(date);
