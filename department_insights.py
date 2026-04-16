"""pages/home.py — Home Page: Project overview + KPI cards."""

import streamlit as st
import pandas as pd
from utils.styles import inject_css, kpi_card, page_hero, section_header, insight_card
from utils.data_loader import get_kpis
from utils import charts


def render(df: pd.DataFrame):
    page_hero(
        "HR Attrition Analytics",
        "Identifying the key drivers of employee turnover in a 1,470-person workforce — "
        "and surfacing data-backed retention strategies for HR leadership.",
        "🏢"
    )

    # ── KPI strip ──────────────────────────────────────────────────────────────
    kpis = get_kpis(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, f"{kpis['total_employees']:,}", "Total Employees", None, "amber"),
        (c2, f"{kpis['attrition_count']:,}", "Employees Left", "Above benchmark", "red"),
        (c3, f"{kpis['attrition_rate']}%", "Attrition Rate", "Benchmark: 10–12%", "red"),
        (c4, f"${kpis['avg_monthly_income']:,.0f}", "Avg Monthly Income", None, "green"),
        (c5, f"{kpis['overtime_pct']}%", "On OverTime", None, "amber"),
    ]
    for col, val, label, delta, color in cards:
        col.markdown(kpi_card(val, label, delta, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout: donut + key findings ────────────────────────────────
    col_left, col_right = st.columns([1, 1.4], gap="large")

    with col_left:
        section_header("Attrition at a Glance")
        st.plotly_chart(charts.attrition_donut(df), use_container_width=True)

    with col_right:
        section_header("Critical Findings")
        findings = [
            ("critical", "🔴 <b>OverTime is the #1 risk signal</b> — employees doing overtime leave at 30.5% vs 10.4% for those who don't. That's a <b>3× multiplier</b>."),
            ("critical", "🔴 <b>Entry-level employees (Job Level 1)</b> exit at 26.3% — the highest of any group. Career path visibility is absent."),
            ("default", "🟡 <b>Ages 18–25</b> have a 34.8% attrition rate. Young talent is the most volatile segment."),
            ("default", "🟡 <b>Sales department</b> attrition (20.6%) is 50% higher than R&D (13.8%)."),
            ("positive", "🟢 <b>$2,046/month income gap</b> between retained vs departed employees — compensation is a direct lever."),
            ("positive", "🟢 <b>Single employees</b> leave at 25.5% vs Divorced at 10.1% — lifestyle flexibility matters."),
        ]
        for variant, text in findings:
            st.markdown(insight_card(text, variant), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bottom row charts ──────────────────────────────────────────────────────
    section_header("Quick Snapshots", "Top patterns from the dataset")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(charts.attrition_by_department(df), use_container_width=True)
    with c2:
        st.plotly_chart(charts.overtime_attrition(df), use_container_width=True)
    with c3:
        st.plotly_chart(charts.attrition_by_job_level(df), use_container_width=True)

    # ── Dataset info strip ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#1a1d2e; border:1px solid rgba(255,255,255,0.06); border-radius:12px;
                padding:1.2rem 1.6rem; margin-top:1rem; display:flex; gap:3rem; flex-wrap:wrap">
        <div><span style="color:#8b90a7; font-size:0.78rem">DATASET</span><br>
             <span style="font-weight:600">IBM HR Analytics (Public)</span></div>
        <div><span style="color:#8b90a7; font-size:0.78rem">RECORDS</span><br>
             <span style="font-weight:600">1,470 Employees · 35 Features</span></div>
        <div><span style="color:#8b90a7; font-size:0.78rem">TARGET</span><br>
             <span style="font-weight:600">Attrition (Yes / No)</span></div>
        <div><span style="color:#8b90a7; font-size:0.78rem">MISSING VALUES</span><br>
             <span style="font-weight:600; color:#3ecf8e">None — Clean Dataset</span></div>
        <div><span style="color:#8b90a7; font-size:0.78rem">AUTHOR</span><br>
             <span style="font-weight:600">Neha Tiwari</span></div>
    </div>
    """, unsafe_allow_html=True)
