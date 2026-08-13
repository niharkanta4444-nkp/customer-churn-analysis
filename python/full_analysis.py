"""
Customer Churn Deep Dive & Retention Action Plan
==================================================
Full analysis pipeline: data cleaning -> EDA -> root cause analysis -> revenue impact

Author: Nihar Kanta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

# ============================================================
# 1. LOAD RAW DATA
# ============================================================
df = pd.read_csv('../data/raw/customer_churn_data.csv')
print("Raw data shape:", df.shape)
print(df.head())
print(df.info())
print(df.isnull().sum())

# ============================================================
# 2. DATA CLEANING
# ============================================================

# 2a. TotalCharges: missing only for brand-new customers (0 tenure) -> fill with 0
df['TotalCharges'] = df['TotalCharges'].fillna(0)

# 2b. PaymentMethod: missing = unknown data entry gap -> label as "Unknown"
df['PaymentMethod'] = df['PaymentMethod'].fillna('Unknown')

# 2c. SupportTickets: missing = no ticket logged -> fill with 0
df['SupportTickets'] = df['SupportTickets'].fillna(0)

# 2d. Gender: fix inconsistent capitalization (e.g. 'FEMALE' vs 'Female')
df['Gender'] = df['Gender'].str.strip().str.capitalize()

# 2e. Remove exact duplicate rows
df = df.drop_duplicates()

# 2f. Fix impossible age values (data entry errors) -> replace with median
median_age = df['Age'].median()
df.loc[(df['Age'] < 18) | (df['Age'] > 100), 'Age'] = median_age

print("\nCleaned data shape:", df.shape)
print("Remaining missing values:\n", df.isnull().sum())

# Save cleaned dataset
df.to_csv('../data/cleaned/customer_churn_cleaned.csv', index=False)


# ============================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================

# --- Q1: Overall churn rate ---
churn_rate = df['Churn'].value_counts(normalize=True) * 100
print("\nOverall churn rate:\n", churn_rate)

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Churn', palette=['#2ecc71', '#e74c3c'])
plt.title('Customer Churn Distribution')
plt.xlabel('Churn')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('../images/01_churn_distribution.png', dpi=150)
plt.close()

# --- Q2: Churn by Contract Type ---
contract_churn = df.groupby('ContractType')['Churn'].value_counts(normalize=True).unstack() * 100
print("\nChurn by Contract Type (%):\n", contract_churn)

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x='ContractType', hue='Churn',
              order=['Month-to-month', 'One year', 'Two year'],
              palette=['#2ecc71', '#e74c3c'])
plt.title('Churn by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Number of Customers')
plt.legend(title='Churned')
plt.tight_layout()
plt.savefig('../images/02_churn_by_contract.png', dpi=150)
plt.close()

# --- Q3: Tenure vs Churn ---
avg_tenure_churn = df.groupby('Churn')['Tenure'].mean()
print("\nAverage tenure by churn status:\n", avg_tenure_churn)

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='Tenure', hue='Churn', multiple='stack',
             palette=['#2ecc71', '#e74c3c'], bins=20)
plt.title('Customer Tenure Distribution by Churn Status')
plt.xlabel('Tenure (months)')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('../images/03_tenure_distribution.png', dpi=150)
plt.close()

# --- Q4: Login Frequency vs Churn ---
avg_login_churn = df.groupby('Churn')['LoginFrequency'].mean()
print("\nAverage login frequency by churn status:\n", avg_login_churn)

plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x='Churn', y='LoginFrequency', palette=['#2ecc71', '#e74c3c'])
plt.title('Login Frequency by Churn Status')
plt.xlabel('Churn')
plt.ylabel('Average Logins per Month')
plt.tight_layout()
plt.savefig('../images/04_login_frequency.png', dpi=150)
plt.close()

# --- Q5: Support Tickets vs Churn ---
avg_tickets_churn = df.groupby('Churn')['SupportTickets'].mean()
print("\nAverage support tickets by churn status:\n", avg_tickets_churn)

high_tickets = df[df['SupportTickets'] >= 3]
churn_rate_high_tickets = high_tickets['Churn'].value_counts(normalize=True) * 100
print("\nChurn rate for customers with 3+ tickets:\n", churn_rate_high_tickets)

plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x='Churn', y='SupportTickets', palette=['#2ecc71', '#e74c3c'])
plt.title('Support Tickets by Churn Status')
plt.xlabel('Churn')
plt.ylabel('Number of Support Tickets')
plt.tight_layout()
plt.savefig('../images/05_support_tickets.png', dpi=150)
plt.close()

# --- Q6: Subscription Type vs Churn ---
subscription_churn = df.groupby('SubscriptionType')['Churn'].value_counts(normalize=True).unstack() * 100
print("\nChurn by Subscription Type (%):\n", subscription_churn)

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x='SubscriptionType', hue='Churn',
              order=['Basic', 'Standard', 'Premium'],
              palette=['#2ecc71', '#e74c3c'])
plt.title('Churn by Subscription Type')
plt.xlabel('Subscription Type')
plt.ylabel('Number of Customers')
plt.legend(title='Churned')
plt.tight_layout()
plt.savefig('../images/06_churn_by_subscription.png', dpi=150)
plt.close()

# --- Q7: Revenue at Risk ---
total_monthly_revenue = df['MonthlyCharges'].sum()
churned_monthly_revenue = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()
revenue_at_risk_pct = (churned_monthly_revenue / total_monthly_revenue) * 100
annual_revenue_lost = churned_monthly_revenue * 12

print(f"\nTotal Monthly Revenue: ${total_monthly_revenue:,.2f}")
print(f"Monthly Revenue Lost to Churn: ${churned_monthly_revenue:,.2f}")
print(f"Percentage of Revenue at Risk: {revenue_at_risk_pct:.1f}%")
print(f"Estimated Annual Revenue Lost: ${annual_revenue_lost:,.2f}")


# ============================================================
# 4. ROOT CAUSE ANALYSIS - Compounding Risk Factors
# ============================================================

# High-risk segment: month-to-month AND 3+ support tickets
high_risk = df[(df['ContractType'] == 'Month-to-month') & (df['SupportTickets'] >= 3)]
churn_rate_high_risk = high_risk['Churn'].value_counts(normalize=True) * 100
print(f"\n--- High Risk Segment (Month-to-month + 3+ tickets) ---")
print(f"Segment size: {len(high_risk)} customers")
print(churn_rate_high_risk)

# Low-risk segment: long contract AND few tickets
low_risk = df[(df['ContractType'] != 'Month-to-month') & (df['SupportTickets'] < 3)]
churn_rate_low_risk = low_risk['Churn'].value_counts(normalize=True) * 100
print(f"\n--- Low Risk Segment (Annual contracts + <3 tickets) ---")
print(f"Segment size: {len(low_risk)} customers")
print(churn_rate_low_risk)

# High-value customers at risk: above-average charges AND churned
avg_charge = df['MonthlyCharges'].mean()
high_value_at_risk = df[(df['MonthlyCharges'] > avg_charge) & (df['Churn'] == 'Yes')]
print(f"\n--- High-Value Customers Who Churned ---")
print(f"Count: {len(high_value_at_risk)}")
print(f"Revenue lost from this segment: ${high_value_at_risk['MonthlyCharges'].sum():,.2f}/month")

print("\n\nAnalysis complete. Charts saved to ../images/. Cleaned data saved to ../data/cleaned/.")
