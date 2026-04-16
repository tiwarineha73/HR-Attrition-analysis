"""pages/attrition_analysis.py — Deep dive into attrition drivers."""

import streamlit as st
import pandas as pd
from utils.styles import page_hero, section_header, kpi_card, insight_card
from utils import charts


def render(df: pd.DataFrame):
    page_hero(
        "Attrition Analysis",
        "A multi-dimensional breakdown of who is leaving and what factors are most strongly associated with departure.",
        "📉"
    )

    # ── Filters ────────────────────────────────────────────────────────────────
    with st.expander("🔧 Filter Data", expanded=False):
        f1, f2, f3 = st.columns(3)
        dept_opts = ["All"] + sorted(df["Department"].unique().tolist())
        gender_opts = ["All"] + sorted(df["Gender"].unique().tolist())
        ot_opts = ["All", "Yes", "No"]
        with f1:
            dept = st.selectbox("Department", dept_opts, key="attr_dept")
        with f2:
            gender = st.selectbox("Gender", gender_opts, key="attr_gender")
        with f3:
            ot = st.selectbox("OverTime", ot_opts, key="attr_ot")

    fdf = df.copy()
    if dept != "All":
        fdf = fdf[fdf["Department"] == dept]
    if gender != "All":
        fdf = fdf[fdf["Gender"] == gender]
    if ot != "All":
        fdf = fdf[fdf["OverTime"] == ot]

    # ── KPI row ────────────────────────────────────────────────────────────────
    total = len(fdf)
    left = int(fdf["AttritionFlag"].sum())
    rate = round(left / total * 100, 1) if total > 0 else 0
    avg_income_left = fdf[fdf["Attrition"] == "Yes"]["MonthlyIncome"].mean()
    avg_income_stay = fdf[fdf["Attrition"] == "No"]["MonthlyIncome"].mean()
    income_gap = avg_income_stay - avg_income_left

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card(f"{total:,}", "Filtered Employees", None, "amber"), unsafe_allow_html=True)
    c2.markdown(kpi_card(f"{left:,}", "Left the Company", None, "red"), unsafe_allow_html=True)
    c3.markdown(kpi_card(f"{rate}%", "Attrition Rate", "Benchmark: 10–12%", "red"), unsafe_allow_html=True)
    c4.markdown(kpi_card(f"${income_gap:,.0f}", "Avg Income Gap (Stay–Left)", None, "green"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1 ──────────────────────────────────────────────────────────────────
    section_header("Attrition by Key Segments")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.attrition_by_age(fdf), use_container_width=True)
    with c2:
        st.plotly_chart(charts.attrition_by_job_level(fdf), use_container_width=True)

    # ── Row 2 ──────────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.overtime_attrition(fdf), use_container_width=True)
    with c2:
        st.plotly_chart(charts.attrition_by_marital(fdf), use_container_width=True)

    # ── Row 3 ──────────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.income_band_attrition(fdf), use_container_width=True)
    with c2:
        st.plotly_chart(charts.attrition_by_tenure(fdf), use_container_width=True)

    # ── Income distribution ────────────────────────────────────────────────────
    section_header("Income Distribution: Who Left vs Who Stayed")
    st.plotly_chart(charts.income_distribution(fdf), use_container_width=True)

    # ── Correlation heatmap ────────────────────────────────────────────────────
    section_header("Feature Correlation Heatmap",
                   "Strength of linear association between numeric features and Attrition (AttritionFlag)")
    st.plotly_chart(charts.correlation_heatmap(fdf), use_container_width=True)

    st.markdown(
        insight_card(
            "⚠️ <b>Interpretation note:</b> Correlation ≠ causation. These are bivariate associations. "
            "A feature that correlates with AttritionFlag may be a proxy for another variable (e.g., "
            "income gap is partly driven by job level). See the Prediction page for model-based feature importance.",
            "default"
        ),
        unsafe_allow_html=True
    )

    # ── Satisfaction analysis ──────────────────────────────────────────────────
    section_header("Job Satisfaction vs Attrition")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.satisfaction_attrition(fdf), use_container_width=True)
    with c2:
        # WorkLifeBalance breakdown
        wlb = (fdf.groupby("WorkLifeBalance")["AttritionFlag"]
               .agg(["mean", "count"]).reset_index()
               .rename(columns={"mean": "rate", "count": "n"}))
        wlb["rate"] = (wlb["rate"] * 100).round(1)
        import plotly.graph_objects as go
        labels = {1: "Bad", 2: "Good", 3: "Better", 4: "Best"}
        wlb["label"] = wlb["WorkLifeBalance"].map(labels)
        AMBER, RED, GREEN, BG, TEXT, MUTED, GRID = "#f5a623", "#e05252", "#3ecf8e", "#1a1d2e", "#f0f2f8", "#8b90a7", "rgba(255,255,255,0.05)"
        colors = [RED if r > 18 else AMBER if r > 14 else GREEN for r in wlb["rate"]]
        fig = go.Figure(go.Bar(
            x=wlb["label"], y=wlb["rate"],
            marker_color=colors,
            text=[f"{r}%<br>n={n}" for r, n in zip(wlb["rate"], wlb["n"])],
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
        ))
        fig.update_layout(
            paper_bgcolor=BG, plot_bgcolor=BG,
            font=dict(family="DM Sans", color=TEXT),
            margin=dict(l=20, r=20, t=50, b=20),
            height=340,
            xaxis=dict(gridcolor=GRID, zeroline=False),
            yaxis=dict(gridcolor=GRID, zeroline=False, range=[0, wlb["rate"].max() + 5]),
            title=dict(text="Attrition by Work-Life Balance Rating", font=dict(size=15, color=TEXT, family="Syne"), x=0.01),
        )
        st.plotly_chart(fig, use_container_width=True)
