# Resume & Interview Prep

## Project Title
**Customer Churn Deep Dive & Retention Action Plan**

## Resume Bullet Points

- Analyzed a 2,000-customer churn dataset using Python and SQL, identifying that customers with both short-term contracts and high support-ticket volume churned at 40.4% — 3.3x the rate of low-risk customers — driving a prioritized retention strategy.
- Cleaned and validated a real-world-style dataset (missing values, duplicates, outliers) in Pandas, applying column-specific logic rather than blanket deletion to preserve ~96% of usable records.
- Quantified $302K in estimated annual revenue at risk from churn and identified that high-value customers accounted for ~70% of that loss, reframing the churn problem in business/revenue terms for stakeholders.
- Built 6+ visualizations (Matplotlib/Seaborn) and SQL queries (CTEs, window functions, aggregations) to answer 8 core business questions, documented in a structured GitHub portfolio project.

## 30-Second Explanation

"I built an end-to-end churn analysis project — cleaned a messy dataset, used SQL and Python to test which factors actually predict churn, and found that contract type and support tickets were the two real drivers. The most useful insight was that customers with *both* risk factors churned at over 3 times the rate of low-risk customers, which let me propose a prioritized retention plan instead of a one-size-fits-all approach."

## 2-Minute Explanation

"The project started with a business problem: a company is losing customers, but doesn't know why or how much it's costing them. I worked with a customer dataset that had realistic data quality issues — missing values, duplicates, incorrect entries — and cleaned it methodically, deciding case-by-case whether to fill, label as unknown, or fix based on why the data was likely missing, rather than just dropping rows.

From there, I ran exploratory analysis in Python to test several business questions: does churn vary by contract type, tenure, usage, support tickets, or subscription tier? I found contract type was the strongest single driver — month-to-month customers churned at nearly 3x the rate of annual contract customers — while some other factors, like login frequency, showed almost no relationship at all, which was an important finding in itself.

The most valuable part was root cause analysis: I tested whether risk factors compound. Customers with both a month-to-month contract and 3+ support tickets churned at 40%, compared to just 12% for low-risk customers — a much sharper signal than any single factor alone. I also quantified the revenue impact: about $300K a year at risk, with high-value customers making up a disproportionate share of that.

I finished by translating this into a concrete action plan — prioritizing retention outreach for the compounding high-risk segment and proposing a contract-conversion incentive — and documented the whole project on GitHub with SQL queries, a Jupyter notebook, and a written findings report."

## Likely Interviewer Questions & Strong Answers

**Q: Why did you use a synthetic dataset instead of real data?**
A: Real company churn data is almost never public for privacy and legal reasons. I built a synthetic dataset designed to mirror realistic churn patterns and data-quality issues, and I disclose that clearly in the README — the analysis techniques and reasoning transfer directly to real data.

**Q: How did you decide how to handle missing values?**
A: I looked at each column individually rather than applying one rule to everything. For example, missing TotalCharges only occurred for brand-new customers with 0 tenure, so filling with 0 was logically correct — not a guess. For PaymentMethod, the gaps looked random, so I labeled them "Unknown" rather than fabricating a value.

**Q: Can you say contract type causes churn?**
A: No — I was careful to describe it as a correlation. Customers with certain characteristics may simply prefer month-to-month contracts, or other confounding factors could be at play. Proving causation would require a controlled experiment, which I didn't have.

**Q: What would you do differently with more time/data?**
A: I'd want transaction-level or interaction-level data (e.g., support ticket resolution time, not just count) to dig deeper into *why* support friction predicts churn. I'd also want to validate the "3+ tickets" threshold against real churn-timing data rather than treating it as a fixed assumption.

**Q: What was the hardest part of this project?**
A: Resisting the urge to over-claim. Several factors I expected to matter (login frequency, subscription tier) turned out to be weak predictors, and reporting that honestly — instead of forcing a story — was more valuable than pretending every variable mattered.
