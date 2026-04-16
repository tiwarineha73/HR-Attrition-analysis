"""pages/data_overview.py — Raw data explorer with filters and stats."""

import streamlit as st
import pandas as pd
from utils.styles import page_hero, section_header, kpi_card


def render(df: pd.DataFrame):
    page_hero(
        "Data Overview",
        "Explore the raw IBM HR dataset — 1,470 employees, 35 features, zero missing values.",
        "📋"
    )

    # ── Filters ────────────────────────────────────────────────────────────────
    section_header("Filters", "Narrow down the dataset for exploration")
    f1, f2, f3, f4 = st.columns(4)

    departments = ["All"] + sorted(df["Department"].unique().tolist())
    genders = ["All"] + sorted(df["Gender"].unique().tolist())
    attrition_opts = ["All", "Yes (Left)", "No (Stayed)"]
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())

    with f1:
        dept = st.selectbox("Department", departments)
    with f2:
        gender = st.selectbox("Gender", genders)
    with f3:
        attrition = st.selectbox("Attrition Status", attrition_opts)
    with f4:
        age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    # Apply filters
    filtered = df.copy()
    if dept != "All":
        filtered = filtered[filtered["Department"] == dept]
    if gender != "All":
        filtered = filtered[filtered["Gender"] == gender]
    if attrition == "Yes (Left)":
        filtered = filtered[filtered["Attrition"] == "Yes"]
    elif attrition == "No (Stayed)":
        filtered = filtered[filtered["Attrition"] == "No"]
    filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]

    # ── Filtered KPIs ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    attr_rate = round(filtered["AttritionFlag"].mean() * 100, 1) if len(filtered) > 0 else 0
    c1.markdown(kpi_card(f"{len(filtered):,}", "Filtered Records", None, "amber"), unsafe_allow_html=True)
    c2.markdown(kpi_card(f"{attr_rate}%", "Attrition Rate", None, "red"), unsafe_allow_html=True)
    c3.markdown(kpi_card(f"${filtered['MonthlyIncome'].mean():,.0f}" if len(filtered) > 0 else "—", "Avg Income", None, "green"), unsafe_allow_html=True)
    c4.markdown(kpi_card(f"{filtered['Age'].mean():.1f}" if len(filtered) > 0 else "—", "Avg Age", None, "blue"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Dataset table ──────────────────────────────────────────────────────────
    section_header("Dataset Preview", f"Showing {min(200, len(filtered))} of {len(filtered)} records")

    display_cols = [
        "EmployeeNumber", "Age", "Gender", "Department", "JobRole",
        "JobLevel", "MonthlyIncome", "OverTime", "YearsAtCompany",
        "JobSatisfaction", "WorkLifeBalance", "Attrition"
    ]
    display_df = filtered[display_cols].head(200).reset_index(drop=True)

    st.dataframe(
        display_df.style.apply(
            lambda col: ["background-color: rgba(224,82,82,0.12); color:#e05252" if v == "Yes"
                         else "background-color: rgba(62,207,142,0.08); color:#3ecf8e" if v == "No"
                         else "" for v in col]
            if col.name == "Attrition" else [""] * len(col),
            axis=0
        ),
        use_container_width=True,
        height=420,
    )

    # ── Descriptive statistics ─────────────────────────────────────────────────
    with st.expander("📊 Descriptive Statistics (Numeric Columns)"):
        num_cols = ["Age", "MonthlyIncome", "DailyRate", "HourlyRate",
                    "TotalWorkingYears", "YearsAtCompany", "JobSatisfaction",
                    "WorkLifeBalance", "EnvironmentSatisfaction"]
        st.dataframe(filtered[num_cols].describe().round(2), use_container_width=True)

    with st.expander("📁 Column Reference Guide"):
        col_info = {
            "Age": "Employee age in years",
            "Attrition": "Whether employee left (Yes) or stayed (No) — Target variable",
            "BusinessTravel": "Frequency of business travel",
            "Department": "Employee's department",
            "DistanceFromHome": "Distance from home to office (miles)",
            "Education": "Education level (1=Below College to 5=Doctor)",
            "EnvironmentSatisfaction": "Satisfaction with work environment (1–4)",
            "JobInvolvement": "Level of job involvement (1–4)",
            "JobLevel": "Seniority level (1=Entry to 5=Executive)",
            "JobSatisfaction": "Satisfaction with job (1–4)",
            "MonthlyIncome": "Monthly salary in USD",
            "OverTime": "Whether employee works overtime (Yes/No)",
            "TotalWorkingYears": "Total career experience in years",
            "WorkLifeBalance": "Work-life balance rating (1–4)",
            "YearsAtCompany": "Tenure at IBM",
            "YearsSinceLastPromotion": "Years since last promotion",
        }
        col_df = pd.DataFrame(
            [(k, v) for k, v in col_info.items()],
            columns=["Column", "Description"]
        )
        st.dataframe(col_df, use_container_width=True, hide_index=True)

    # ── Download button ────────────────────────────────────────────────────────
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="hr_attrition_filtered.csv",
        mime="text/csv",
    )
