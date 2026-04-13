# =============================================================================
# HR Employee Attrition Analysis
# Author: Neha Tiwari
# Dataset: IBM HR Analytics (1,470 employee records, 35 features)
# Goal: Identify key drivers of employee attrition and provide
#       actionable retention recommendations for HR leadership.
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# Output directory for saving charts
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.family"] = "DejaVu Sans"

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
df = pd.read_csv("../data/HR_Analytics_Data.csv")
print(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: DATA CLEANING & VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

# 3.1 Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
df = df.drop_duplicates()

# 3.2 Missing values check
missing = df.isnull().sum()
print(f"\nMissing values per column:\n{missing[missing > 0]}")
# Result: No missing values in this dataset — confirmed clean.

# 3.3 Drop columns with zero variance (no analytical value)
# 'EmployeeCount' = 1 for all rows, 'StandardHours' = 80 for all, 'Over18' = 'Y' for all
zero_var_cols = ["EmployeeCount", "StandardHours", "Over18"]
df = df.drop(columns=zero_var_cols)
print(f"\nDropped zero-variance columns: {zero_var_cols}")

# 3.4 Encode binary target variable for correlation analysis
df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})

# 3.5 Encode OverTime as binary
df["OverTimeFlag"] = df["OverTime"].map({"Yes": 1, "No": 0})

# 3.6 Create Age Groups for segment analysis
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[18, 25, 35, 45, 60],
    labels=["18–25", "26–35", "36–45", "46–60"],
)

# 3.7 Create Income Bands
df["IncomeBand"] = pd.cut(
    df["MonthlyIncome"],
    bins=[0, 3000, 6000, 10000, 20000],
    labels=["Low (<3K)", "Mid (3K–6K)", "High (6K–10K)", "Very High (>10K)"],
)

print("\n✅ Data cleaning complete.")
print(f"Final dataset shape: {df.shape}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: EXPLORATORY DATA ANALYSIS (EDA)
# ─────────────────────────────────────────────────────────────────────────────

# ── 4.1 Overall Attrition Rate ───────────────────────────────────────────────
total = len(df)
attrition_count = df["Attrition"].value_counts()
attrition_rate = attrition_count["Yes"] / total * 100

print(f"\n── ATTRITION OVERVIEW ──")
print(f"Total Employees  : {total}")
print(f"Left (Attrition) : {attrition_count['Yes']} ({attrition_rate:.1f}%)")
print(f"Retained         : {attrition_count['No']} ({100 - attrition_rate:.1f}%)")

# ── 4.2 Attrition by Department ─────────────────────────────────────────────
dept_attr = (
    df.groupby("Department")["AttritionFlag"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
    .rename(columns={"AttritionFlag": "AttritionRate_%"})
    .sort_values("AttritionRate_%", ascending=False)
)
print(f"\n── ATTRITION BY DEPARTMENT ──\n{dept_attr.to_string(index=False)}")

# ── 4.3 Attrition by Job Level ───────────────────────────────────────────────
joblevel_attr = (
    df.groupby("JobLevel")["AttritionFlag"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
    .rename(columns={"AttritionFlag": "AttritionRate_%"})
)
print(f"\n── ATTRITION BY JOB LEVEL ──\n{joblevel_attr.to_string(index=False)}")

# ── 4.4 Attrition by OverTime ────────────────────────────────────────────────
ot_attr = (
    df.groupby("OverTime")["AttritionFlag"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
    .rename(columns={"AttritionFlag": "AttritionRate_%"})
)
print(f"\n── ATTRITION BY OVERTIME ──\n{ot_attr.to_string(index=False)}")

# ── 4.5 Average Monthly Income: Stayed vs Left ───────────────────────────────
income_attr = df.groupby("Attrition")["MonthlyIncome"].mean().round(0)
print(f"\n── AVG MONTHLY INCOME (Stayed vs Left) ──\n{income_attr}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────────────────

# ── Chart 1: Overall Attrition Distribution ─────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))
colors = ["#2ECC71", "#E74C3C"]
bars = ax.bar(
    attrition_count.index,
    attrition_count.values,
    color=colors,
    edgecolor="white",
    linewidth=1.5,
    width=0.5,
)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 10,
        f"{bar.get_height():,}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )
ax.set_title("Overall Employee Attrition", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Attrition", fontsize=11)
ax.set_ylabel("Number of Employees", fontsize=11)
ax.set_ylim(0, 1400)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_overall_attrition.png")
plt.close()
print("Chart 1 saved.")

# ── Chart 2: Attrition Rate by Department ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
palette = sns.color_palette("Reds_d", len(dept_attr))
bars = ax.barh(
    dept_attr["Department"],
    dept_attr["AttritionRate_%"],
    color=palette,
    edgecolor="white",
)
for bar in bars:
    ax.text(
        bar.get_width() + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{bar.get_width():.1f}%",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_title("Attrition Rate by Department", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Attrition Rate (%)", fontsize=11)
ax.set_xlim(0, 30)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_attrition_by_department.png")
plt.close()
print("Chart 2 saved.")

# ── Chart 3: Attrition by Age Group ─────────────────────────────────────────
age_attr = (
    df.groupby("AgeGroup", observed=True)["AttritionFlag"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(7, 5))
palette = sns.color_palette("OrRd", len(age_attr))
bars = ax.bar(
    age_attr["AgeGroup"].astype(str),
    age_attr["AttritionFlag"],
    color=palette,
    edgecolor="white",
    width=0.5,
)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{bar.get_height():.1f}%",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_title("Attrition Rate by Age Group", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Attrition Rate (%)", fontsize=11)
ax.set_ylim(0, 45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_attrition_by_age.png")
plt.close()
print("Chart 3 saved.")

# ── Chart 4: Income Distribution — Stayed vs Left ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
for label, color in [("No", "#2ECC71"), ("Yes", "#E74C3C")]:
    subset = df[df["Attrition"] == label]["MonthlyIncome"]
    sns.kdeplot(subset, ax=ax, label=f"Attrition={label}", color=color, fill=True, alpha=0.35)
ax.set_title(
    "Monthly Income Distribution: Stayed vs Left", fontsize=14, fontweight="bold", pad=15
)
ax.set_xlabel("Monthly Income (USD)", fontsize=11)
ax.set_ylabel("Density", fontsize=11)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_income_distribution.png")
plt.close()
print("Chart 4 saved.")

# ── Chart 5: OverTime Impact on Attrition ───────────────────────────────────
ot_cross = pd.crosstab(df["OverTime"], df["Attrition"], normalize="index").mul(100).round(1)
fig, ax = plt.subplots(figsize=(6, 5))
ot_cross.plot(
    kind="bar",
    ax=ax,
    color=["#2ECC71", "#E74C3C"],
    edgecolor="white",
    width=0.5,
)
ax.set_title("OverTime vs Attrition Rate", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("OverTime", fontsize=11)
ax.set_ylabel("Percentage (%)", fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Attrition", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_overtime_attrition.png")
plt.close()
print("Chart 5 saved.")

# ── Chart 6: Attrition by Marital Status ────────────────────────────────────
marital_attr = (
    df.groupby("MaritalStatus")["AttritionFlag"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
    .rename(columns={"AttritionFlag": "AttritionRate_%"})
    .sort_values("AttritionRate_%", ascending=False)
)
fig, ax = plt.subplots(figsize=(6, 5))
palette = sns.color_palette("YlOrRd", len(marital_attr))
bars = ax.bar(
    marital_attr["MaritalStatus"],
    marital_attr["AttritionRate_%"],
    color=palette,
    edgecolor="white",
    width=0.5,
)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{bar.get_height():.1f}%",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_title("Attrition Rate by Marital Status", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Marital Status", fontsize=11)
ax.set_ylabel("Attrition Rate (%)", fontsize=11)
ax.set_ylim(0, 33)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_attrition_by_marital_status.png")
plt.close()
print("Chart 6 saved.")

# ── Chart 7: Attrition by Job Level ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
palette = sns.color_palette("flare", len(joblevel_attr))
bars = ax.bar(
    joblevel_attr["JobLevel"].astype(str),
    joblevel_attr["AttritionRate_%"],
    color=palette,
    edgecolor="white",
    width=0.5,
)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.4,
        f"{bar.get_height():.1f}%",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_title("Attrition Rate by Job Level", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Job Level (1=Entry, 5=Executive)", fontsize=11)
ax.set_ylabel("Attrition Rate (%)", fontsize=11)
ax.set_ylim(0, 33)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_attrition_by_job_level.png")
plt.close()
print("Chart 7 saved.")

# ── Chart 8: Correlation Heatmap ─────────────────────────────────────────────
numeric_cols = [
    "AttritionFlag", "Age", "MonthlyIncome", "OverTimeFlag",
    "TotalWorkingYears", "YearsAtCompany", "JobLevel",
    "JobSatisfaction", "WorkLifeBalance", "EnvironmentSatisfaction",
    "YearsSinceLastPromotion", "NumCompaniesWorked",
]
corr = df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(11, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr,
    mask=mask,
    annot=True,
    fmt=".2f",
    cmap="RdYlGn",
    center=0,
    ax=ax,
    linewidths=0.5,
    cbar_kws={"shrink": 0.8},
)
ax.set_title(
    "Feature Correlation Heatmap (vs Attrition)", fontsize=14, fontweight="bold", pad=15
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_correlation_heatmap.png")
plt.close()
print("Chart 8 saved.")

print("\n✅ All charts saved to /outputs/")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: KEY INSIGHTS SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("""
═══════════════════════════════════════════════════════════════
                     KEY BUSINESS INSIGHTS
═══════════════════════════════════════════════════════════════

1. OVERALL ATTRITION: 16.1% of employees left — above the
   typical healthy benchmark of 10–12% for mid-size companies.

2. OVERTIME IS THE #1 RISK FACTOR:
   - Employees doing overtime: 30.5% attrition rate
   - Employees NOT doing overtime: 10.4% attrition rate
   - That's a 3x higher risk — the strongest signal in the data.

3. ENTRY-LEVEL EMPLOYEES LEAVE MOST:
   - Job Level 1: 26.3% attrition — highest of all levels
   - Job Level 4: 4.7% attrition — lowest
   - Entry roles need better career path visibility and mentoring.

4. YOUNG EMPLOYEES ARE HIGH-RISK:
   - Age 18–25: 34.8% attrition
   - Age 26–35: 19.1% attrition
   - These two groups account for majority of talent loss.

5. SALES DEPARTMENT NEEDS ATTENTION:
   - Sales: 20.6% attrition vs R&D: 13.8%
   - Sales Executives and Reps face higher pressure and turnover.

6. INCOME GAP IS SIGNIFICANT:
   - Employees who stayed:  avg $6,833/month
   - Employees who left:    avg $4,787/month
   - ~$2,000/month gap suggests compensation is a retention lever.

7. SINGLE EMPLOYEES LEAVE MORE:
   - Single: 25.5% attrition vs Divorced: 10.1%
   - Single employees may have fewer financial commitments,
     making job-switching lower-risk for them.

═══════════════════════════════════════════════════════════════
""")
