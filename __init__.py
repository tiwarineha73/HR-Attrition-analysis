"""pages/department_insights.py — Department-level deep dive."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import page_hero, section_header, kpi_card, insight_card
from utils import charts

BG = "#1a1d2e"
TEXT = "#f0f2f8"
MUTED = "#8b90a7"
GRID = "rgba(255,255,255,0.05)"
AMBER = "#f5a623"
RED = "#e05252"
GREEN = "#3ecf8e"
BLUE = "#4da6ff"
PALETTE = [AMBER, RED, GREEN, BLUE, "#a78bfa", "#f472b6"]


def _layout(fig, title="", h=360):
    d = dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="DM Sans", color=TEXT, size=12),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
        height=h,
    )
    if title:
        d["title"] = dict(text=title, font=dict(size=15, color=TEXT, family="Syne"), x=0.01)
    fig.update_layout(**d)
    return fig


def render(df: pd.DataFrame):
    page_hero(
        "Department Insights",
        "Compare attrition, pay, and satisfaction across Sales, R&D, and Human Resources.",
        "🏬"
    )

    # ── Department selector ────────────────────────────────────────────────────
    departments = sorted(df["Department"].unique().tolist())
    selected_dept = st.radio(
        "Select Department for Deep Dive",
        ["All Departments"] + departments,
        horizontal=True,
    )

    fdf = df if selected_dept == "All Departments" else df[df["Department"] == selected_dept]

    # ── KPI row ────────────────────────────────────────────────────────────────
    total = len(fdf)
    left = int(fdf["AttritionFlag"].sum())
    rate = round(left / total * 100, 1)
    avg_income = fdf["MonthlyIncome"].mean()
    avg_sat = fdf["JobSatisfaction"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi_card(f"{total:,}", "Headcount", None, "amber"), unsafe_allow_html=True)
    c2.markdown(kpi_card(f"{left:,}", "Employees Lost", None, "red"), unsafe_allow_html=True)
    c3.markdown(kpi_card(f"{rate}%", "Attrition Rate", None, "red"), unsafe_allow_html=True)
    c4.markdown(kpi_card(f"${avg_income:,.0f}", "Avg Monthly Income", None, "green"), unsafe_allow_html=True)
    c5.markdown(kpi_card(f"{avg_sat:.2f}/4", "Avg Job Satisfaction", None, "blue"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Department comparison ──────────────────────────────────────────────────
    section_header("Department Comparison")
    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(charts.attrition_by_department(df), use_container_width=True)

    with c2:
        st.plotly_chart(charts.dept_headcount(df), use_container_width=True)

    # ── Job role analysis ──────────────────────────────────────────────────────
    section_header("Job Role Analysis", "Bubble size = number of employees who left")
    st.plotly_chart(charts.job_role_bubble(fdf), use_container_width=True)

    # ── Job role attrition table ───────────────────────────────────────────────
    section_header("Job Role Attrition Detail")
    role_data = (fdf.groupby("JobRole")["AttritionFlag"]
                 .agg(["mean", "count", "sum"])
                 .reset_index()
                 .rename(columns={"mean": "Attrition Rate", "count": "Total", "sum": "Employees Lost"}))
    role_data["Attrition Rate"] = (role_data["Attrition Rate"] * 100).round(1).astype(str) + "%"
    role_data = role_data.sort_values("Employees Lost", ascending=False)
    st.dataframe(role_data.reset_index(drop=True), use_container_width=True, hide_index=True)

    # ── Salary by department ───────────────────────────────────────────────────
    section_header("Compensation Analysis")
    c1, c2 = st.columns(2)

    with c1:
        dept_income = (df.groupby("Department")["MonthlyIncome"].mean().reset_index()
                       .rename(columns={"MonthlyIncome": "AvgIncome"}))
        fig = go.Figure(go.Bar(
            x=dept_income["Department"],
            y=dept_income["AvgIncome"].round(0),
            marker_color=PALETTE[:len(dept_income)],
            text=[f"${v:,.0f}" for v in dept_income["AvgIncome"]],
            textposition="outside",
            textfont=dict(size=12, color=TEXT),
        ))
        fig.update_yaxes(range=[0, dept_income["AvgIncome"].max() + 1000])
        st.plotly_chart(_layout(fig, "Avg Monthly Income by Department", h=340), use_container_width=True)

    with c2:
        # Salary gap: attrited vs retained by dept
        gap = (df.groupby(["Department", "Attrition"])["MonthlyIncome"]
               .mean().round(0).reset_index())
        fig = go.Figure()
        for attr, color, name in [("No", GREEN, "Retained"), ("Yes", RED, "Attrited")]:
            subset = gap[gap["Attrition"] == attr]
            fig.add_trace(go.Bar(
                x=subset["Department"],
                y=subset["MonthlyIncome"],
                name=name,
                marker_color=color,
                text=[f"${v:,.0f}" for v in subset["MonthlyIncome"]],
                textposition="inside",
                textfont=dict(size=11, color="#fff"),
            ))
        fig.update_layout(barmode="group")
        st.plotly_chart(_layout(fig, "Income: Retained vs Attrited by Dept", h=340), use_container_width=True)

    # ── Travel impact ──────────────────────────────────────────────────────────
    section_header("Business Travel Impact")
    travel_attr = (fdf.groupby("BusinessTravel")["AttritionFlag"]
                   .agg(["mean", "count"]).reset_index()
                   .rename(columns={"mean": "rate", "count": "n"}))
    travel_attr["rate"] = (travel_attr["rate"] * 100).round(1)
    travel_attr = travel_attr.sort_values("rate", ascending=False)
    colors = [RED if r > 20 else AMBER if r > 12 else GREEN for r in travel_attr["rate"]]

    fig = go.Figure(go.Bar(
        x=travel_attr["BusinessTravel"],
        y=travel_attr["rate"],
        marker_color=colors,
        text=[f"{r}%<br>n={n}" for r, n in zip(travel_attr["rate"], travel_attr["n"])],
        textposition="outside",
        textfont=dict(size=12, color=TEXT),
    ))
    fig.update_yaxes(range=[0, travel_attr["rate"].max() + 5])
    st.plotly_chart(_layout(fig, "Attrition Rate by Business Travel Frequency", h=340), use_container_width=True)

    st.markdown(
        insight_card(
            "💡 Frequent travelers leave at the highest rate. This should be factored into role design, "
            "not just compensation — travel fatigue is a real retention risk especially in Sales roles.",
            "default"
        ),
        unsafe_allow_html=True
    )
