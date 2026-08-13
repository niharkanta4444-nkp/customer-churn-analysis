# Customer Churn Deep Dive & Retention Action Plan

A data analytics project investigating why customers churn, quantifying the business/revenue impact, and producing a data-backed retention action plan.

## Business Problem

A subscription-based company is losing customers, but management doesn't know how much churn is happening, which customers are leaving, why, or what to do about it. This project answers those questions using SQL, Python, and data visualization — moving from **data → analysis → root cause → business insight → action plan.**

## Dataset

This project uses a **synthetic dataset** (2,000 customers) generated to closely mirror real-world telecom/subscription churn patterns — realistic churn rate (~25%), correlated risk factors (contract type, support tickets), and intentional data-quality issues (missing values, duplicates, outliers) to reflect the kind of messy data analysts work with in practice.

| Column | Description |
|---|---|
| CustomerID | Unique customer identifier |
| Gender | Male / Female |
| Age | Customer age |
| Tenure | Months as a customer |
| SubscriptionType | Basic / Standard / Premium |
| ContractType | Month-to-month / One year / Two year |
| MonthlyCharges | Monthly billed amount |
| TotalCharges | Total billed to date |
| PaymentMethod | How the customer pays |
| LoginFrequency | Average logins per month |
| SupportTickets | Number of support tickets raised |
| LastActiveDate | Most recent activity date |
| Churn | Yes/No — did the customer leave? |

## Tools Used

- **Python** (Pandas, Matplotlib, Seaborn) — data cleaning and exploratory analysis
- **PostgreSQL** — business-question SQL queries
- **Jupyter Notebook** — analysis workflow
- **Git/GitHub** — version control and portfolio hosting

## Project Structure

```
customer-churn-analysis/
├── data/
│   ├── raw/              # Original, unmodified dataset
│   └── cleaned/          # Cleaned dataset after processing
├── sql/                  # SQL analysis queries
├── python/                # Jupyter notebook with full analysis
├── images/                # Saved chart exports
├── reports/                # Written findings and action plan
└── README.md
```

## Key Findings

1. **Overall churn rate: ~25%** — roughly 1 in 4 customers has left.
2. **Contract type is the strongest churn driver.** Month-to-month customers churn at ~33%, vs. ~12-14% for annual contracts.
3. **Support friction is a moderate, real driver.** Customers with 3+ support tickets churn at 30%, above the 25% baseline.
4. **Tenure, login frequency, and subscription tier are weak/negligible drivers** on their own.
5. **Risk factors compound.** Customers with both a month-to-month contract and 3+ support tickets churn at **40.4%**, vs. just **12.1%** for customers with an annual contract and few tickets — a **3.3x difference**.
6. **Revenue at risk: ~$25,177/month (~$302K/year)**, with high-value customers (above-average charges) accounting for roughly 70% of that lost revenue.

## Recommendations

| Risk Signal | Recommended Action |
|---|---|
| Month-to-month contract | Offer incentives to convert to annual contracts |
| 3+ support tickets | Proactive support outreach / account review |
| Both combined (highest risk) | Priority retention outreach — contract offer + service recovery |
| High-value churned customers | Priority win-back campaign |

## Limitations

- Dataset is synthetic, not real company data — patterns are realistic but not guaranteed to match any specific business.
- Findings describe **correlation, not proven causation** — no controlled experiment was run.
- Risk thresholds (e.g., "3+ tickets") are analytical assumptions based on where churn increases in this dataset, and should be validated against real operational data before use.

## How to Reproduce

1. Clone this repository
2. Install dependencies: `pip install pandas numpy matplotlib seaborn openpyxl`
3. Open `python/01_churn_analysis.ipynb` in VS Code or Jupyter
4. Run all cells — this regenerates the cleaned dataset and all charts
5. (Optional) Load `data/cleaned/customer_churn_cleaned.csv` into PostgreSQL and run `sql/churn_analysis_queries.sql`
