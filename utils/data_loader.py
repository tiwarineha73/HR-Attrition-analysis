"""
data_loader.py — Centralized data loading, cleaning, and feature engineering.
All pages import from here to ensure consistency.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "HR_Analytics_Data.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean the HR dataset. Cached so it only runs once per session."""
    df = pd.read_csv(DATA_PATH)

    # ── Drop zero-variance columns ─────────────────────────────────────────────
    df = df.drop(columns=["EmployeeCount", "StandardHours", "Over18"], errors="ignore")

    # ── Binary encoding ────────────────────────────────────────────────────────
    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})
    df["OverTimeFlag"] = df["OverTime"].map({"Yes": 1, "No": 0})

    # ── Derived segments ───────────────────────────────────────────────────────
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 60],
        labels=["18–25", "26–35", "36–45", "46–60"],
    )
    df["IncomeBand"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 3000, 6000, 10000, 20000],
        labels=["Low (<$3K)", "Mid ($3K–$6K)", "High ($6K–$10K)", "Very High (>$10K)"],
    )
    df["TenureBand"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 1, 3, 5, 10, 40],
        labels=["0–1 yrs", "2–3 yrs", "4–5 yrs", "6–10 yrs", "10+ yrs"],
    )

    return df


@st.cache_data
def get_kpis(df: pd.DataFrame) -> dict:
    """Return top-level KPI metrics."""
    total = len(df)
    left = df["AttritionFlag"].sum()
    return {
        "total_employees": total,
        "attrition_count": int(left),
        "retention_count": int(total - left),
        "attrition_rate": round(left / total * 100, 1),
        "avg_monthly_income": round(df["MonthlyIncome"].mean(), 0),
        "avg_age": round(df["Age"].mean(), 1),
        "overtime_pct": round(df["OverTimeFlag"].mean() * 100, 1),
    }
