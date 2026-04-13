# HR Employee Attrition Analysis

**Identifying Key Drivers of Employee Turnover Using Python & Power BI**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green?logo=pandas)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## Project Overview

Employee attrition is one of the most costly HR challenges for any organization. Replacing a single employee can cost **50–200% of their annual salary** when factoring in recruitment, onboarding, and lost productivity.

This project analyzes **1,470 employee records** across 35 features to identify the primary drivers behind employee attrition — and deliver actionable, data-backed retention strategies to HR leadership.

---

## Business Problem Statement

> *"The HR team has observed a 16.1% annual attrition rate — exceeding the industry benchmark of 10–12%. Leadership needs to understand which employee segments are leaving, why, and what interventions can reduce turnover before it impacts business performance."*

---

## Objectives

- Calculate the overall attrition rate and benchmark it against industry standards
- Identify which departments, job levels, and age groups have the highest attrition risk
- Quantify the impact of overtime, compensation, and job satisfaction on attrition
- Build an interactive Power BI dashboard for HR leadership reporting
- Deliver actionable, prioritized retention recommendations

---

## Dataset Description

| Attribute        | Detail                                              |
|------------------|-----------------------------------------------------|
| **Source**       | IBM HR Analytics Dataset (publicly available)       |
| **Records**      | 1,470 employees                                     |
| **Features**     | 35 columns (demographic, job, satisfaction, tenure) |
| **Target**       | `Attrition` (Yes/No — binary classification)       |
| **Format**       | CSV (tab-delimited)                                 |
| **Missing Data** | None — dataset is complete                         |

**Key Features Used:**

- `Age`, `Gender`, `MaritalStatus`
- `Department`, `JobRole`, `JobLevel`
- `MonthlyIncome`, `PercentSalaryHike`, `DailyRate`
- `OverTime`, `WorkLifeBalance`, `JobSatisfaction`
- `YearsAtCompany`, `TotalWorkingYears`, `YearsSinceLastPromotion`

---

## Tools & Technologies

| Category           | Tools Used                            |
|--------------------|---------------------------------------|
| Language           | Python 3.10+                          |
| Data Processing    | Pandas, NumPy                         |
| Visualization      | Matplotlib, Seaborn                   |
| Dashboard          | Power BI                              |
| SQL Analysis       | MySQL / Standard SQL                  |
| Version Control    | Git, GitHub                           |
| Environment        | Jupyter Notebook / VS Code            |

---

## Project Workflow

```
Raw CSV Data
     │
     ▼
Data Cleaning & Validation
(duplicates, zero-variance cols, type casting, feature engineering)
     │
     ▼
Exploratory Data Analysis
(attrition by dept, level, age, overtime, income, tenure)
     │
     ▼
Python Visualizations (8 charts)
     │
     ▼
SQL Business Queries (10 queries)
     │
     ▼
Power BI Dashboard
     │
     ▼
Key Insights & Recommendations
```

---

## Key Insights

| # | Finding | Impact |
|---|---------|--------|
| 1 | **Overall attrition: 16.1%** — above the healthy 10–12% benchmark | High |
| 2 | **OverTime employees: 30.5% attrition** vs 10.4% for non-overtime — 3× higher risk | Critical |
| 3 | **Job Level 1 (Entry): 26.3% attrition** — highest of all levels | Critical |
| 4 | **Age 18–25: 34.8% attrition** — nearly 1 in 3 young employees leaves | High |
| 5 | **Sales dept: 20.6% attrition** vs R&D: 13.8% | High |
| 6 | **Salary gap: $2,046/month** between retained vs attrited employees | High |
| 7 | **Single employees: 25.5% attrition** vs Divorced: 10.1% | Medium |

---

## Visualizations Generated

| File | Description |
|------|-------------|
| `01_overall_attrition.png` | Bar chart of attrition vs retention count |
| `02_attrition_by_department.png` | Horizontal bar — attrition rate by department |
| `03_attrition_by_age.png` | Attrition rate across 4 age groups |
| `04_income_distribution.png` | KDE plot — income distribution: stayed vs left |
| `05_overtime_attrition.png` | Stacked bar — overtime impact on attrition |
| `06_attrition_by_marital_status.png` | Attrition rate by marital status |
| `07_attrition_by_job_level.png` | Attrition rate by job level (1–5) |
| `08_correlation_heatmap.png` | Feature correlation heatmap vs attrition |

---

## Recommendations

1. **Cap Overtime Immediately**
   Implement a policy limiting overtime to ≤10 hrs/week. The 3× attrition multiplier for overtime employees is the single most actionable lever available.

2. **Launch an Entry-Level Retention Program**
   Job Level 1 employees (26.3% attrition) need structured 90-day onboarding, a clear 12-month career path, and a mentorship pairing system.

3. **Increase Compensation for Bottom Quartile**
   Employees earning below $3,000/month are the most vulnerable. A targeted 10–15% salary review for this group reduces financial pull-factors.

4. **Invest in Sales Team Support**
   Sales attrition at 20.6% signals workload or incentive structure issues. Introduce performance bonuses, realistic target-setting, and mental health support.

5. **Create Early-Tenure Checkpoints**
   Employees in years 0–2 have the highest exit risk. Structured 30-60-90 day check-ins and stay interviews at 6 months can flag at-risk employees early.

---

## Project Structure

```
hr-attrition-analysis/
│
├── data/
│   └── HR_Analytics_Data.csv          # Raw dataset (1,470 rows × 35 cols)
│
├── notebooks/
│   └── hr_attrition_analysis.py       # Full analysis script (runnable)
│
├── src/
│   └── hr_analysis_queries.sql        # 10 business SQL queries
│
├── outputs/
│   ├── 01_overall_attrition.png
│   ├── 02_attrition_by_department.png
│   ├── 03_attrition_by_age.png
│   ├── 04_income_distribution.png
│   ├── 05_overtime_attrition.png
│   ├── 06_attrition_by_marital_status.png
│   ├── 07_attrition_by_job_level.png
│   └── 08_correlation_heatmap.png
│
├── docs/
│   └── HR_Dashboard_PowerBI.jpg       # Power BI dashboard screenshot
│
├── README.md
└── requirements.txt
```

---

## How to Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/tiwarineha73/hr-attrition-analysis.git
cd hr-attrition-analysis
```

**Step 2 — Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Run the analysis**
```bash
cd notebooks
python hr_attrition_analysis.py
```

**Step 5 — View outputs**
All charts will be saved automatically to the `/outputs/` folder.

---

## Power BI Dashboard

The dashboard (screenshot in `/docs/`) was built with the same dataset and displays:
- Total headcount: 1,470 | Male: 60% | Female: 40%
- Promotion eligibility: 72 due (4.9%) | 1,398 not due (95.1%)
- Active workers: 1,353 (92%) | Next retrenchment: 117 (8%)
- Service years distribution (bar chart)
- Job level distribution (bar chart)
- Distance from office segmentation (donut chart)

---

## Author

**Neha Tiwari**
Data Analyst | Python • SQL • Power BI • Machine Learning

- GitHub: [github.com/tiwarineha73](https://github.com/tiwarineha73)
- LinkedIn: [linkedin.com/in/neha-tiwari](https://linkedin.com/in/neha-tiwari)
- Email: tiwari.neha3111@gmail.com

---

*This project is part of an end-to-end data analytics portfolio built on real datasets.*
