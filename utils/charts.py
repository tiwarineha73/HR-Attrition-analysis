"""
charts.py — Reusable Plotly chart factory functions.
All charts follow the dark corporate theme.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Shared theme ───────────────────────────────────────────────────────────────
BG = "#1a1d2e"
PAPER = "#1a1d2e"
GRID = "rgba(255,255,255,0.05)"
TEXT = "#f0f2f8"
MUTED = "#8b90a7"
AMBER = "#f5a623"
RED = "#e05252"
GREEN = "#3ecf8e"
BLUE = "#4da6ff"
PALETTE = [AMBER, RED, GREEN, BLUE, "#a78bfa", "#f472b6", "#34d399", "#60a5fa"]

LAYOUT_BASE = dict(
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(family="DM Sans", color=TEXT, size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
    yaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
)


def _apply_layout(fig, title="", height=400):
    layout = dict(**LAYOUT_BASE, height=height)
    if title:
        layout["title"] = dict(text=title, font=dict(size=15, color=TEXT, family="Syne"), x=0.01)
    fig.update_layout(**layout)
    return fig


# ── 1. Attrition donut ────────────────────────────────────────────────────────
def attrition_donut(df):
    counts = df["Attrition"].value_counts()
    fig = go.Figure(go.Pie(
        labels=["Retained", "Attrited"],
        values=[counts.get("No", 0), counts.get("Yes", 0)],
        hole=0.65,
        marker=dict(colors=[GREEN, RED], line=dict(color=BG, width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, color=TEXT),
    ))
    total = len(df)
    rate = round(counts.get("Yes", 0) / total * 100, 1)
    fig.add_annotation(text=f"<b>{rate}%</b><br><span style='font-size:11px;color:{MUTED}'>Attrition</span>",
                       x=0.5, y=0.5, showarrow=False, font=dict(size=20, color=AMBER))
    return _apply_layout(fig, "Overall Attrition Rate", height=360)


# ── 2. Attrition by department (horizontal bar) ────────────────────────────────
def attrition_by_department(df):
    data = (df.groupby("Department")["AttritionFlag"].agg(["mean", "count"])
            .reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    data = data.sort_values("rate")
    colors = [RED if r > 18 else AMBER if r > 14 else GREEN for r in data["rate"]]
    fig = go.Figure(go.Bar(
        x=data["rate"], y=data["Department"],
        orientation="h",
        marker_color=colors,
        text=[f"{r}%  (n={n})" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.update_xaxes(range=[0, data["rate"].max() + 5])
    return _apply_layout(fig, "Attrition Rate by Department", height=300)


# ── 3. Attrition by age group ──────────────────────────────────────────────────
def attrition_by_age(df):
    data = (df.groupby("AgeGroup", observed=True)["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=data["AgeGroup"].astype(str),
        y=data["rate"],
        marker_color=PALETTE[:len(data)],
        text=[f"{r}%<br><span style='font-size:10px'>n={n}</span>" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.update_yaxes(range=[0, data["rate"].max() + 6])
    return _apply_layout(fig, "Attrition Rate by Age Group", height=360)


# ── 4. Income KDE by attrition ────────────────────────────────────────────────
def income_distribution(df):
    fig = go.Figure()
    for label, color, name in [("No", GREEN, "Retained"), ("Yes", RED, "Attrited")]:
        subset = df[df["Attrition"] == label]["MonthlyIncome"]
        fig.add_trace(go.Violin(
            x=subset, name=name,
            line_color=color,
            fillcolor=color.replace(")", ",0.15)").replace("rgb", "rgba") if "rgb" in color else color + "26",
            opacity=0.8, meanline_visible=True, side="positive",
            points=False, bandwidth=400,
        ))
    fig.update_layout(violinmode="overlay")
    return _apply_layout(fig, "Monthly Income: Retained vs Attrited", height=360)


# ── 5. Overtime vs attrition (grouped bar) ─────────────────────────────────────
def overtime_attrition(df):
    cross = pd.crosstab(df["OverTime"], df["Attrition"], normalize="index").mul(100).round(1)
    fig = go.Figure()
    for col, color, name in [("No", GREEN, "Retained"), ("Yes", RED, "Attrited")]:
        fig.add_trace(go.Bar(
            x=cross.index, y=cross[col], name=name,
            marker_color=color,
            text=[f"{v:.1f}%" for v in cross[col]],
            textposition="inside",
            textfont=dict(size=12, color="#fff"),
        ))
    fig.update_layout(barmode="stack")
    return _apply_layout(fig, "OverTime vs Attrition (%)", height=340)


# ── 6. Job level attrition ────────────────────────────────────────────────────
def attrition_by_job_level(df):
    data = (df.groupby("JobLevel")["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    colors = [RED if r > 20 else AMBER if r > 10 else GREEN for r in data["rate"]]
    fig = go.Figure(go.Bar(
        x=data["JobLevel"].astype(str),
        y=data["rate"],
        marker_color=colors,
        text=[f"{r}%<br>n={n}" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    level_labels = ["1 - Entry", "2 - Junior", "3 - Mid", "4 - Senior", "5 - Executive"]
    fig.update_xaxes(tickvals=list(range(1, 6)), ticktext=level_labels)
    fig.update_yaxes(range=[0, data["rate"].max() + 6])
    return _apply_layout(fig, "Attrition Rate by Job Level", height=360)


# ── 7. Correlation heatmap ────────────────────────────────────────────────────
def correlation_heatmap(df):
    cols = [
        "AttritionFlag", "Age", "MonthlyIncome", "OverTimeFlag",
        "TotalWorkingYears", "YearsAtCompany", "JobLevel",
        "JobSatisfaction", "WorkLifeBalance", "EnvironmentSatisfaction",
        "YearsSinceLastPromotion", "NumCompaniesWorked",
    ]
    corr = df[cols].corr().round(2)
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdYlGn",
        zmid=0, zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text}",
        textfont=dict(size=9),
        colorbar=dict(thickness=12, tickfont=dict(color=MUTED)),
    ))
    return _apply_layout(fig, "Feature Correlation Heatmap", height=520)


# ── 8. Job role attrition bubble chart ────────────────────────────────────────
def job_role_bubble(df):
    data = (df.groupby("JobRole")["AttritionFlag"]
            .agg(["mean", "count", "sum"]).reset_index()
            .rename(columns={"mean": "rate", "count": "total", "sum": "lost"}))
    data["rate"] = (data["rate"] * 100).round(1)
    data = data.sort_values("rate", ascending=False)
    fig = px.scatter(
        data, x="total", y="rate", size="lost",
        color="rate", color_continuous_scale=["#3ecf8e", "#f5a623", "#e05252"],
        text="JobRole",
        hover_data={"total": True, "lost": True, "rate": True},
        labels={"total": "Total Employees", "rate": "Attrition Rate (%)"},
    )
    fig.update_traces(textposition="top center", textfont=dict(size=9, color=TEXT))
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, "Job Role: Size = Employees Lost", height=440)


# ── 9. Marital status attrition ───────────────────────────────────────────────
def attrition_by_marital(df):
    data = (df.groupby("MaritalStatus")["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    data = data.sort_values("rate", ascending=False)
    colors = [RED if r > 20 else AMBER if r > 12 else GREEN for r in data["rate"]]
    fig = go.Figure(go.Bar(
        x=data["MaritalStatus"], y=data["rate"],
        marker_color=colors,
        text=[f"{r}%<br>n={n}" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.update_yaxes(range=[0, data["rate"].max() + 5])
    return _apply_layout(fig, "Attrition by Marital Status", height=340)


# ── 10. Tenure band attrition ─────────────────────────────────────────────────
def attrition_by_tenure(df):
    order = ["0–1 yrs", "2–3 yrs", "4–5 yrs", "6–10 yrs", "10+ yrs"]
    data = (df.groupby("TenureBand", observed=True)["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    data["TenureBand"] = pd.Categorical(data["TenureBand"], categories=order, ordered=True)
    data = data.sort_values("TenureBand")
    fig = go.Figure(go.Scatter(
        x=data["TenureBand"].astype(str), y=data["rate"],
        mode="lines+markers+text",
        line=dict(color=AMBER, width=3),
        marker=dict(size=10, color=AMBER, line=dict(color=BG, width=2)),
        text=[f"{r}%" for r in data["rate"]],
        textposition="top center",
        textfont=dict(color=TEXT, size=11),
    ))
    fig.add_hrect(y0=10, y1=12, fillcolor="rgba(62,207,142,0.05)",
                  line_width=0, annotation_text="Healthy benchmark", annotation_font_color=MUTED)
    return _apply_layout(fig, "Attrition Rate by Company Tenure", height=360)


# ── 11. Gender split ──────────────────────────────────────────────────────────
def gender_attrition(df):
    data = (df.groupby("Gender")["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=data["Gender"], y=data["rate"],
        marker_color=[BLUE, AMBER],
        text=[f"{r}%<br>n={n}" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=12, color=TEXT),
    ))
    fig.update_yaxes(range=[0, data["rate"].max() + 5])
    return _apply_layout(fig, "Attrition by Gender", height=320)


# ── 12. Age distribution histogram ───────────────────────────────────────────
def age_distribution(df):
    fig = go.Figure()
    for label, color, name in [("No", GREEN, "Retained"), ("Yes", RED, "Attrited")]:
        subset = df[df["Attrition"] == label]["Age"]
        fig.add_trace(go.Histogram(
            x=subset, name=name,
            marker_color=color,
            opacity=0.75, nbinsx=20,
        ))
    fig.update_layout(barmode="overlay")
    return _apply_layout(fig, "Age Distribution by Attrition Status", height=360)


# ── 13. Income band attrition ─────────────────────────────────────────────────
def income_band_attrition(df):
    order = ["Low (<$3K)", "Mid ($3K–$6K)", "High ($6K–$10K)", "Very High (>$10K)"]
    data = (df.groupby("IncomeBand", observed=True)["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    data["IncomeBand"] = pd.Categorical(data["IncomeBand"], categories=order, ordered=True)
    data = data.sort_values("IncomeBand")
    colors = [RED if r > 20 else AMBER if r > 12 else GREEN for r in data["rate"]]
    fig = go.Figure(go.Bar(
        x=data["IncomeBand"].astype(str),
        y=data["rate"],
        marker_color=colors,
        text=[f"{r}%<br>n={n}" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.update_yaxes(range=[0, data["rate"].max() + 6])
    return _apply_layout(fig, "Attrition by Income Band", height=360)


# ── 14. Department headcount stacked bar ──────────────────────────────────────
def dept_headcount(df):
    data = pd.crosstab(df["Department"], df["Attrition"])
    fig = go.Figure()
    for col, color, name in [("No", GREEN, "Retained"), ("Yes", RED, "Attrited")]:
        if col in data.columns:
            fig.add_trace(go.Bar(
                x=data.index, y=data[col], name=name,
                marker_color=color,
                text=data[col],
                textposition="inside",
                textfont=dict(size=11, color="#fff"),
            ))
    fig.update_layout(barmode="stack")
    return _apply_layout(fig, "Headcount by Department", height=340)


# ── 15. Job satisfaction vs attrition ────────────────────────────────────────
def satisfaction_attrition(df):
    data = (df.groupby("JobSatisfaction")["AttritionFlag"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "n"}))
    data["rate"] = (data["rate"] * 100).round(1)
    labels = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    data["label"] = data["JobSatisfaction"].map(labels)
    colors = [RED if r > 18 else AMBER if r > 14 else GREEN for r in data["rate"]]
    fig = go.Figure(go.Bar(
        x=data["label"], y=data["rate"],
        marker_color=colors,
        text=[f"{r}%<br>n={n}" for r, n in zip(data["rate"], data["n"])],
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig.update_yaxes(range=[0, data["rate"].max() + 5])
    return _apply_layout(fig, "Attrition by Job Satisfaction Level", height=340)
