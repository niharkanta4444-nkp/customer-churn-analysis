# Customer Churn Analysis — Findings Summary

## Headline Numbers

- **Churn rate:** 24.75% (~1 in 4 customers)
- **Monthly revenue lost to churn:** $25,176.55
- **Annualized revenue lost:** ~$302,119
- **Highest-risk segment churn rate:** 40.4% (month-to-month + 3+ support tickets)
- **Lowest-risk segment churn rate:** 12.1% (annual contract + <3 tickets)

## What Drives Churn (Ranked by Strength)

1. **Contract type — Strong.** Month-to-month customers churn at 33.4%, vs. 11.9% (one year) and 14.1% (two year).
2. **Support tickets — Moderate.** Customers with 3+ tickets churn at 30%, vs. ~25% baseline.
3. **Tenure — Weak.** Churned customers average 34 months vs. 37 for retained — a small gap.
4. **Subscription type — Weak.** All tiers churn within a few points of the 25% baseline.
5. **Login frequency — Negligible.** Almost no difference between churned and retained customers.

## Root Cause: Compounding Risk

Testing combinations of risk factors reveals a much sharper signal than any single variable:

- **High-risk segment** (month-to-month + 3+ tickets): 146 customers, **40.4% churn**
- **Low-risk segment** (annual contract + <3 tickets): 721 customers, **12.1% churn**

This 3.3x gap is the strongest evidence in the dataset, and the clearest basis for a targeted retention strategy — rather than treating all customers the same.

## Revenue Impact Detail

- 242 high-value customers (above-average MonthlyCharges) churned.
- These customers alone account for $17,580.72/month in lost revenue — about 70% of total revenue lost to churn.
- This means churn isn't just a volume problem — it's disproportionately affecting the most valuable accounts.

## Recommended Action Plan

1. **Contract conversion campaign:** Target month-to-month customers with incentives (discount, added features) to move to annual contracts.
2. **Proactive support review:** Flag any customer reaching 3 support tickets for a manual account review before they reach a churn decision point.
3. **Compounding-risk priority queue:** Customers matching *both* risk factors should be the top priority for retention outreach — combine a contract offer with direct service recovery.
4. **High-value win-back:** Build a targeted win-back list (see SQL query 8) ranking churned customers by revenue, and prioritize outreach accordingly.
5. **Onboarding review:** Given the (modest) tenure effect, consider strengthening the first-90-days onboarding experience.

## Limitations & Caveats

- All findings are **correlational**, based on observational data — not a controlled experiment. Statements are phrased as "customers with X show higher churn," not "X causes churn."
- The dataset is synthetic, built to mirror realistic patterns, not real company data.
- The "3+ tickets" and "above-average charges" thresholds are analytical choices based on where patterns emerged in this data, not fixed business rules.
