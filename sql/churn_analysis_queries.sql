-- =====================================================================
-- Customer Churn Deep Dive & Retention Action Plan
-- SQL Analysis Queries (PostgreSQL)
--
-- Before running: import data/cleaned/customer_churn_cleaned.csv into
-- a table named "customers" using pgAdmin's Import/Export tool, or:
--
--   CREATE TABLE customers (
--       CustomerID        TEXT,
--       Gender            TEXT,
--       Age               INT,
--       Tenure            INT,
--       SubscriptionType  TEXT,
--       ContractType      TEXT,
--       MonthlyCharges    NUMERIC,
--       TotalCharges      NUMERIC,
--       PaymentMethod     TEXT,
--       LoginFrequency    INT,
--       SupportTickets    INT,
--       LastActiveDate    DATE,
--       Churn             TEXT
--   );
--
--   \copy customers FROM 'data/cleaned/customer_churn_cleaned.csv' DELIMITER ',' CSV HEADER;
-- =====================================================================


-- ---------------------------------------------------------------------
-- Q1: What is the overall churn rate?
-- ---------------------------------------------------------------------
SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_total
FROM customers
GROUP BY churn;


-- ---------------------------------------------------------------------
-- Q2: How does churn vary by contract type?
-- ---------------------------------------------------------------------
SELECT
    contracttype,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customers
GROUP BY contracttype
ORDER BY churn_rate_pct DESC;


-- ---------------------------------------------------------------------
-- Q3: Does tenure affect churn? (average tenure by churn status)
-- ---------------------------------------------------------------------
SELECT
    churn,
    ROUND(AVG(tenure), 1) AS avg_tenure_months,
    MIN(tenure) AS min_tenure,
    MAX(tenure) AS max_tenure
FROM customers
GROUP BY churn;


-- ---------------------------------------------------------------------
-- Q4: Do support tickets relate to churn?
-- ---------------------------------------------------------------------
SELECT
    churn,
    ROUND(AVG(supporttickets), 2) AS avg_support_tickets
FROM customers
GROUP BY churn;

-- Churn rate specifically for customers with 3+ support tickets
SELECT
    COUNT(*) AS segment_size,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customers
WHERE supporttickets >= 3;


-- ---------------------------------------------------------------------
-- Q5: Which subscription type has the highest churn?
-- ---------------------------------------------------------------------
SELECT
    subscriptiontype,
    COUNT(*) AS total_customers,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customers
GROUP BY subscriptiontype
ORDER BY churn_rate_pct DESC;


-- ---------------------------------------------------------------------
-- Q6: How much monthly revenue is at risk from churned customers?
-- ---------------------------------------------------------------------
SELECT
    ROUND(SUM(monthlycharges), 2) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthlycharges ELSE 0 END), 2) AS revenue_lost_to_churn,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN monthlycharges ELSE 0 END) / SUM(monthlycharges),
        1
    ) AS pct_revenue_at_risk
FROM customers;


-- ---------------------------------------------------------------------
-- Q7 (Root Cause): Compounding risk -- month-to-month AND 3+ tickets
-- Uses a CTE to build the high-risk segment, then compares against
-- everyone else.
-- ---------------------------------------------------------------------
WITH risk_segment AS (
    SELECT
        *,
        CASE
            WHEN contracttype = 'Month-to-month' AND supporttickets >= 3 THEN 'High Risk'
            WHEN contracttype != 'Month-to-month' AND supporttickets < 3 THEN 'Low Risk'
            ELSE 'Medium Risk'
        END AS risk_segment
    FROM customers
)
SELECT
    risk_segment,
    COUNT(*) AS segment_size,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM risk_segment
GROUP BY risk_segment
ORDER BY churn_rate_pct DESC;


-- ---------------------------------------------------------------------
-- Q8: Rank customers by revenue lost, for the highest-value churned
-- customers (useful for a targeted win-back list)
-- ---------------------------------------------------------------------
SELECT
    customerid,
    contracttype,
    subscriptiontype,
    monthlycharges,
    supporttickets,
    RANK() OVER (ORDER BY monthlycharges DESC) AS revenue_rank
FROM customers
WHERE churn = 'Yes'
ORDER BY monthlycharges DESC
LIMIT 20;
