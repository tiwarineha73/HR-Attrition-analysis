"""pages/prediction.py — Attrition Prediction using Random Forest."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import page_hero, section_header, kpi_card, insight_card
from utils.ml_model import train_model, predict_employee, CATEGORICAL_COLS

BG = "#1a1d2e"
TEXT = "#f0f2f8"
MUTED = "#8b90a7"
GRID = "rgba(255,255,255,0.05)"
AMBER = "#f5a623"
RED = "#e05252"
GREEN = "#3ecf8e"


def render(df: pd.DataFrame):
    page_hero(
        "Attrition Predictor",
        "A Random Forest classifier trained on 1,470 records. Enter employee details to predict attrition risk.",
        "🤖"
    )

    # ── Train model ────────────────────────────────────────────────────────────
    with st.spinner("Training Random Forest model..."):
        model, encoders, metrics = train_model(df)

    # ── Model metrics ──────────────────────────────────────────────────────────
    section_header("Model Performance", "Evaluated on 20% holdout test set")
    c1, c2, c3, c4 = st.columns(4)
    report = metrics["report"]
    c1.markdown(kpi_card(f"{metrics['accuracy']}%", "Accuracy", None, "green"), unsafe_allow_html=True)
    c2.markdown(kpi_card(f"{metrics['roc_auc']}%", "ROC-AUC Score", None, "amber"), unsafe_allow_html=True)
    c3.markdown(kpi_card(f"{round(report['1']['precision']*100,1)}%", "Precision (Attrition)", None, "blue"), unsafe_allow_html=True)
    c4.markdown(kpi_card(f"{round(report['1']['recall']*100,1)}%", "Recall (Attrition)", None, "red"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature importance ─────────────────────────────────────────────────────
    section_header("Top Feature Importances", "What the model actually uses to predict attrition")
    fi = metrics["feature_importance"].head(12).sort_values()
    colors = [AMBER if v > fi.median() else "#4da6ff" for v in fi.values]

    fig = go.Figure(go.Bar(
        x=fi.values, y=fi.index,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.3f}" for v in fi.values],
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="DM Sans", color=TEXT),
        margin=dict(l=20, r=60, t=40, b=20),
        height=400,
        xaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED)),
        title=dict(text="Feature Importance (Random Forest)", font=dict(size=15, color=TEXT, family="Syne"), x=0.01),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        insight_card(
            "📌 Unlike simple correlation, feature importance from a tree model accounts for "
            "<b>joint effects</b> across all variables. MonthlyIncome, Age, and OverTime consistently "
            "dominate — aligning with the EDA findings but now with more statistical rigour.",
            "default"
        ),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Prediction form ────────────────────────────────────────────────────────
    section_header("🔮 Predict for an Employee", "Fill in the details below")

    with st.form("prediction_form"):
        st.markdown("**Personal & Role Information**")
        r1c1, r1c2, r1c3, r1c4 = st.columns(4)
        age = r1c1.slider("Age", 18, 60, 32)
        monthly_income = r1c2.number_input("Monthly Income ($)", 1000, 20000, 5000, step=500)
        job_level = r1c3.selectbox("Job Level", [1, 2, 3, 4, 5], index=0)
        dept = r1c4.selectbox("Department", CATEGORICAL_COLS["Department"])

        r2c1, r2c2, r2c3, r2c4 = st.columns(4)
        job_role = r2c1.selectbox("Job Role", CATEGORICAL_COLS["JobRole"])
        gender = r2c2.selectbox("Gender", CATEGORICAL_COLS["Gender"])
        marital = r2c3.selectbox("Marital Status", CATEGORICAL_COLS["MaritalStatus"])
        overtime = r2c4.selectbox("OverTime", CATEGORICAL_COLS["OverTime"])

        st.markdown("**Experience & Tenure**")
        r3c1, r3c2, r3c3, r3c4 = st.columns(4)
        total_yrs = r3c1.slider("Total Working Years", 0, 40, 8)
        yrs_company = r3c2.slider("Years at Company", 0, 40, 5)
        yrs_role = r3c3.slider("Years in Current Role", 0, 18, 3)
        yrs_promo = r3c4.slider("Years Since Last Promotion", 0, 15, 2)

        st.markdown("**Satisfaction & Work Style**")
        r4c1, r4c2, r4c3, r4c4 = st.columns(4)
        job_sat = r4c1.select_slider("Job Satisfaction", [1, 2, 3, 4], value=3)
        env_sat = r4c2.select_slider("Environment Satisfaction", [1, 2, 3, 4], value=3)
        wlb = r4c3.select_slider("Work-Life Balance", [1, 2, 3, 4], value=3)
        travel = r4c4.selectbox("Business Travel", CATEGORICAL_COLS["BusinessTravel"])

        st.markdown("**Compensation & Other**")
        r5c1, r5c2, r5c3, r5c4 = st.columns(4)
        daily_rate = r5c1.number_input("Daily Rate", 100, 1500, 800, step=50)
        hourly_rate = r5c2.number_input("Hourly Rate", 30, 100, 65, step=5)
        monthly_rate = r5c3.number_input("Monthly Rate", 2000, 27000, 14000, step=1000)
        pct_hike = r5c4.slider("% Salary Hike", 11, 25, 14)

        r6c1, r6c2, r6c3, r6c4 = st.columns(4)
        num_companies = r6c1.slider("Num Companies Worked", 0, 9, 2)
        stock_option = r6c2.selectbox("Stock Option Level", [0, 1, 2, 3])
        training = r6c3.slider("Training Times Last Year", 0, 6, 2)
        edu = r6c4.selectbox("Education Field", CATEGORICAL_COLS["EducationField"])

        r7c1, r7c2, r7c3, r7c4 = st.columns(4)
        edu_level = r7c1.selectbox("Education Level (1–5)", [1, 2, 3, 4, 5], index=2)
        job_inv = r7c2.select_slider("Job Involvement", [1, 2, 3, 4], value=3)
        rel_sat = r7c3.select_slider("Relationship Satisfaction", [1, 2, 3, 4], value=3)
        perf_rating = r7c4.selectbox("Performance Rating", [3, 4])

        dist_home = st.slider("Distance from Home (miles)", 1, 29, 9)
        yrs_mgr = st.slider("Years with Current Manager", 0, 17, 4)

        submitted = st.form_submit_button("🔍 Predict Attrition Risk", use_container_width=True)

    if submitted:
        input_dict = {
            "Age": age, "DailyRate": daily_rate, "DistanceFromHome": dist_home,
            "Education": edu_level, "EnvironmentSatisfaction": env_sat,
            "HourlyRate": hourly_rate, "JobInvolvement": job_inv,
            "JobLevel": job_level, "JobSatisfaction": job_sat,
            "MonthlyIncome": monthly_income, "MonthlyRate": monthly_rate,
            "NumCompaniesWorked": num_companies, "PercentSalaryHike": pct_hike,
            "PerformanceRating": perf_rating, "RelationshipSatisfaction": rel_sat,
            "StockOptionLevel": stock_option, "TotalWorkingYears": total_yrs,
            "TrainingTimesLastYear": training, "WorkLifeBalance": wlb,
            "YearsAtCompany": yrs_company, "YearsInCurrentRole": yrs_role,
            "YearsSinceLastPromotion": yrs_promo, "YearsWithCurrManager": yrs_mgr,
            "BusinessTravel": travel, "Department": dept,
            "EducationField": edu, "Gender": gender,
            "JobRole": job_role, "MaritalStatus": marital, "OverTime": overtime,
        }

        result = predict_employee(model, encoders, input_dict)

        # ── Result display ──────────────────────────────────────────────────────
        if result["label"] == "Will Leave":
            css_class = "pred-result will-leave"
            icon = "🔴"
            color = RED
        else:
            css_class = "pred-result will-stay"
            icon = "🟢"
            color = GREEN

        st.markdown(f"""
        <div class="{css_class}">
            <div class="pred-icon">{icon}</div>
            <div class="pred-label" style="color:{color}">{result['label']}</div>
            <div style="font-size:1.1rem; color:{color}; margin:0.3rem 0">{result['risk_level']}</div>
            <div class="pred-prob">Attrition Probability: <b style="color:{color}">{result['probability']}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["probability"],
            number=dict(suffix="%", font=dict(size=32, color=color, family="Syne")),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=MUTED, tickfont=dict(color=MUTED)),
                bar=dict(color=color, thickness=0.3),
                bgcolor=BG,
                borderwidth=0,
                steps=[
                    dict(range=[0, 45], color="rgba(62,207,142,0.1)"),
                    dict(range=[45, 70], color="rgba(245,166,35,0.1)"),
                    dict(range=[70, 100], color="rgba(224,82,82,0.1)"),
                ],
                threshold=dict(line=dict(color=color, width=3), thickness=0.8, value=result["probability"]),
            ),
            domain=dict(x=[0, 1], y=[0, 1]),
        ))
        fig.update_layout(
            paper_bgcolor=BG, font=dict(family="DM Sans", color=TEXT),
            height=280, margin=dict(l=30, r=30, t=30, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        if result["probability"] >= 70:
            note = "⚠️ <b>High attrition risk.</b> Immediate intervention recommended: compensation review, career path discussion, workload assessment."
            variant = "critical"
        elif result["probability"] >= 45:
            note = "🟡 <b>Moderate risk.</b> Consider a stay interview and check in on job satisfaction and growth opportunities."
            variant = "default"
        else:
            note = "✅ <b>Low attrition risk.</b> Employee appears stable. Continue regular engagement and recognition."
            variant = "positive"

        st.markdown(insight_card(note, variant), unsafe_allow_html=True)

    # ── Model disclaimer ───────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📌 Model Assumptions & Limitations"):
        st.markdown("""
        - Trained on IBM HR Analytics dataset — a **synthetic, controlled dataset** not from a real company.
        - Random Forest with `class_weight='balanced'` to handle the 16% attrition minority class.
        - No hyperparameter tuning beyond basic depth/leaf constraints. AUC can be improved with XGBoost + grid search.
        - Predictions are probabilistic, not deterministic. Do not use as the sole decision-making tool.
        - The model does not account for external factors (market conditions, industry, city, role scarcity).
        """)
