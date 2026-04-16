"""pages/conclusion.py — Key insights and retention recommendations."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import page_hero, section_header, insight_card, kpi_card

BG = "#1a1d2e"
TEXT = "#f0f2f8"
MUTED = "#8b90a7"
AMBER = "#f5a623"
RED = "#e05252"
GREEN = "#3ecf8e"
GRID = "rgba(255,255,255,0.05)"


def render(df: pd.DataFrame):
    page_hero(
        "Conclusions & Recommendations",
        "Translating data into action — five prioritised retention interventions for HR leadership.",
        "💡"
    )

    # ── Summary KPIs ───────────────────────────────────────────────────────────
    section_header("What the Data Tells Us")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card("16.1%", "Overall Attrition", "Above 10–12% benchmark", "red"), unsafe_allow_html=True)
    c2.markdown(kpi_card("3×", "OverTime Risk Multiplier", "30.5% vs 10.4%", "red"), unsafe_allow_html=True)
    c3.markdown(kpi_card("26.3%", "Entry Level (L1) Rate", "Highest of any group", "amber"), unsafe_allow_html=True)
    c4.markdown(kpi_card("$2,046", "Monthly Income Gap", "Retained vs Departed", "green"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recommendations ────────────────────────────────────────────────────────
    section_header("5 Prioritised Retention Interventions")

    recs = [
        ("critical", "🔴 PRIORITY 1 — Cap Overtime",
         "The 3× attrition multiplier for overtime workers is the single most actionable lever. "
         "Implement a policy limiting overtime to ≤10 hrs/week. Identify which teams are systematically "
         "understaffed and address the root cause, not just the symptom."),
        ("critical", "🔴 PRIORITY 2 — Entry-Level Retention Program",
         "26.3% of Level 1 employees leave. They need: structured 90-day onboarding, a clear 12-month "
         "career progression path, and a mentorship pairing system. Currently they have none of these — "
         "they are being onboarded into ambiguity."),
        ("default", "🟡 PRIORITY 3 — Targeted Compensation Review",
         "Employees earning below $3,000/month are the most vulnerable. A 10–15% salary review "
         "for this segment costs significantly less than recruitment + onboarding (50–200% of annual salary). "
         "This is a simple ROI-positive move."),
        ("default", "🟡 PRIORITY 4 — Sales Department Intervention",
         "Sales attrition at 20.6% — 50% higher than R&D — signals workload or incentive structure issues. "
         "Introduce realistic target-setting, performance bonuses, and mental health support. "
         "High-travel sales roles carry additional fatigue risk."),
        ("positive", "🟢 PRIORITY 5 — Early-Tenure Check-in Protocol",
         "Employees in years 0–2 have the highest exit risk. Implement mandatory stay interviews "
         "at 30, 60, 90, and 180 days. This catches dissatisfaction before it becomes a resignation letter. "
         "Low cost, high signal."),
    ]

    for variant, title, body in recs:
        st.markdown(insight_card(f"<b>{title}</b><br>{body}", variant), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Risk matrix ────────────────────────────────────────────────────────────
    section_header("Risk vs Impact Matrix",
                   "Where should HR invest first? Impact = employee count at risk × attrition rate")

    interventions = pd.DataFrame({
        "Intervention": [
            "Cap Overtime", "Entry-Level Program", "Salary Review",
            "Sales Dept Support", "Early-Tenure Check-ins",
        ],
        "Implementation Ease (1=Hard, 10=Easy)": [5, 7, 6, 6, 9],
        "Estimated Impact (%)": [30, 20, 15, 12, 10],
        "Urgency": ["Critical", "Critical", "High", "High", "Medium"],
    })

    colors = {"Critical": RED, "High": AMBER, "Medium": GREEN}
    marker_colors = [colors[u] for u in interventions["Urgency"]]

    fig = go.Figure(go.Scatter(
        x=interventions["Implementation Ease (1=Hard, 10=Easy)"],
        y=interventions["Estimated Impact (%)"],
        mode="markers+text",
        marker=dict(size=20, color=marker_colors, line=dict(color=BG, width=2)),
        text=interventions["Intervention"],
        textposition="top center",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.add_vline(x=6, line_dash="dash", line_color=MUTED, opacity=0.4)
    fig.add_hline(y=15, line_dash="dash", line_color=MUTED, opacity=0.4)
    fig.add_annotation(x=9.2, y=28, text="Quick Wins →", font=dict(color=GREEN, size=11), showarrow=False)
    fig.add_annotation(x=3.5, y=28, text="← Big Bets", font=dict(color=RED, size=11), showarrow=False)

    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="DM Sans", color=TEXT),
        margin=dict(l=20, r=20, t=50, b=40),
        height=440,
        xaxis=dict(title="Implementation Ease →", gridcolor=GRID, zeroline=False, range=[3, 11]),
        yaxis=dict(title="Estimated Impact on Attrition (%)", gridcolor=GRID, zeroline=False, range=[5, 35]),
        title=dict(text="Retention Intervention Matrix", font=dict(size=15, color=TEXT, family="Syne"), x=0.01),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Expected ROI ───────────────────────────────────────────────────────────
    section_header("Expected Cost of Inaction")
    left = int(df["AttritionFlag"].sum())
    avg_salary = df["MonthlyIncome"].mean() * 12
    replacement_cost_low = left * avg_salary * 0.5
    replacement_cost_high = left * avg_salary * 2.0

    st.markdown(f"""
    <div style="background:#1a1d2e; border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:1.8rem 2rem; margin-top:0.5rem">
        <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; margin-bottom:1rem">
            Estimated Annual Cost of Current 16.1% Attrition
        </div>
        <div style="display:flex; gap:3rem; flex-wrap:wrap">
            <div>
                <div style="color:{MUTED}; font-size:0.78rem; text-transform:uppercase">Employees Lost / Year</div>
                <div style="font-size:1.8rem; font-weight:800; color:{RED}">{left:,}</div>
            </div>
            <div>
                <div style="color:{MUTED}; font-size:0.78rem; text-transform:uppercase">Avg Annual Salary</div>
                <div style="font-size:1.8rem; font-weight:800; color:{AMBER}">${avg_salary:,.0f}</div>
            </div>
            <div>
                <div style="color:{MUTED}; font-size:0.78rem; text-transform:uppercase">Replacement Cost (50–200%)</div>
                <div style="font-size:1.8rem; font-weight:800; color:{RED}">${replacement_cost_low/1e6:.1f}M – ${replacement_cost_high/1e6:.1f}M</div>
            </div>
        </div>
        <div style="margin-top:1.2rem; font-size:0.85rem; color:{MUTED}">
            Replacement cost = recruitment + onboarding + productivity loss during ramp-up.
            Even a 3% reduction in attrition (to 13%) saves an estimated
            <b style="color:{GREEN}">${(replacement_cost_low * 0.19)/1e6:.1f}M – ${(replacement_cost_high * 0.19)/1e6:.1f}M annually</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Methodology note ───────────────────────────────────────────────────────
    with st.expander("📌 Methodology & Limitations"):
        st.markdown("""
        **What this analysis does:**
        - Descriptive EDA identifying univariate and bivariate patterns across 35 features
        - Predictive model (Random Forest) for attrition probability estimation
        - Cross-tabulation and group comparison of attrition rates

        **What this analysis does NOT do:**
        - Establish causal relationships (e.g., overtime causes attrition vs. both are caused by understaffing)
        - Account for external labour market conditions
        - Control for multicollinearity across features in the EDA section

        **Dataset limitation:**
        - IBM HR Analytics is a synthetic dataset — patterns are plausible but not drawn from a real company's HR records.
        - Real-world deployment would require company-specific data and recalibration.

        **Author:** Neha Tiwari | [github.com/tiwarineha73](https://github.com/tiwarineha73)
        """)
