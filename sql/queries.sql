-- ============================================================
-- Bluestock Mutual Fund Analytics — 10 Analytical Queries
-- ============================================================

-- 1. Top 5 funds by AUM (from scheme_performance)
SELECT amfi_code, scheme_name, fund_house, category,
       aum_crore
  FROM fact_performance
 ORDER BY aum_crore DESC
 LIMIT 5;

-- 2. Average NAV per month for the top 5 schemes by AUM
WITH top5 AS (
    SELECT amfi_code
      FROM fact_performance
     ORDER BY aum_crore DESC
     LIMIT 5
)
SELECT fn.amfi_code,
       df.scheme_name,
       SUBSTR(fn.nav_date, 1, 7) AS month,
       ROUND(AVG(fn.nav), 4)     AS avg_nav
  FROM fact_nav fn
  JOIN dim_fund df ON fn.amfi_code = df.amfi_code
 WHERE fn.amfi_code IN (SELECT amfi_code FROM top5)
 GROUP BY fn.amfi_code, df.scheme_name, SUBSTR(fn.nav_date, 1, 7)
 ORDER BY fn.amfi_code, month;

-- 3. SIP inflow YoY growth rate
SELECT month,
       sip_inflow_crore,
       yoy_growth_pct
  FROM fact_sip_industry
 WHERE yoy_growth_pct IS NOT NULL
 ORDER BY month;

-- 4. Total transactions by state (top 10)
SELECT state,
       COUNT(*)           AS total_transactions,
       ROUND(SUM(amount_inr), 2) AS total_amount_inr
  FROM fact_transactions
 GROUP BY state
 ORDER BY total_transactions DESC
 LIMIT 10;

-- 5. Funds with expense_ratio < 1%
SELECT amfi_code, scheme_name, fund_house,
       expense_ratio_pct
  FROM fact_performance
 WHERE expense_ratio_pct < 1.0
 ORDER BY expense_ratio_pct ASC;

-- 6. Top performing fund per category (by 3yr return)
SELECT fp.category,
       fp.amfi_code,
       fp.scheme_name,
       fp.return_3yr_pct
  FROM fact_performance fp
 INNER JOIN (
     SELECT category, MAX(return_3yr_pct) AS max_3yr
       FROM fact_performance
      GROUP BY category
 ) best ON fp.category = best.category
        AND fp.return_3yr_pct = best.max_3yr
 ORDER BY fp.return_3yr_pct DESC;

-- 7. Monthly transaction volume trend
SELECT SUBSTR(transaction_date, 1, 7) AS month,
       COUNT(*)                        AS num_transactions,
       ROUND(SUM(amount_inr), 2)      AS total_amount_inr
  FROM fact_transactions
 GROUP BY SUBSTR(transaction_date, 1, 7)
 ORDER BY month;

-- 8. Average SIP amount by age group
SELECT age_group,
       COUNT(*)                    AS sip_count,
       ROUND(AVG(amount_inr), 2)  AS avg_sip_amount
  FROM fact_transactions
 WHERE transaction_type = 'SIP'
 GROUP BY age_group
 ORDER BY avg_sip_amount DESC;

-- 9. Fund houses by total AUM (latest quarter)
SELECT fund_house,
       ROUND(SUM(aum_crore), 2)     AS total_aum_crore,
       ROUND(SUM(aum_lakh_crore), 2) AS total_aum_lakh_crore
  FROM fact_aum
 WHERE date = (SELECT MAX(date) FROM fact_aum)
 GROUP BY fund_house
 ORDER BY total_aum_crore DESC;

-- 10. Benchmark comparison: fund 3yr return vs benchmark 3yr return
SELECT amfi_code,
       scheme_name,
       category,
       return_3yr_pct,
       benchmark_3yr_pct,
       ROUND(return_3yr_pct - benchmark_3yr_pct, 2) AS excess_return_pct
  FROM fact_performance
 ORDER BY excess_return_pct DESC;
