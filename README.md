# 🏢 HR Attrition Analytics — Streamlit Web App

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-1.3+-orange?logo=scikit-learn)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-blue?logo=plotly)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

A **multi-page, production-grade Streamlit application** that transforms IBM HR Analytics data into an interactive executive dashboard — with an embedded Random Forest attrition predictor.

---

## 🔥 Live Features

| Page | What's Inside |
|------|--------------|
| 🏠 **Home** | KPI cards, attrition donut, key findings, quick snapshot charts |
| 📋 **Data Overview** | Filterable data table, descriptive stats, column guide, CSV download |
| 📉 **Attrition Analysis** | 10+ Plotly charts — age, income, overtime, tenure, satisfaction, heatmap |
| 👥 **Demographics** | Gender, age, education, income, marital status breakdowns |
| 🏬 **Department Insights** | Dept comparison, job role bubble chart, travel impact, salary gap |
| 🤖 **Attrition Predictor** | Random Forest model — live input form → probability gauge + risk level |
| 💡 **Conclusions** | Prioritised recommendations, risk matrix, cost-of-inaction estimate |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/tiwarineha73/hr-attrition-streamlit.git
cd hr-attrition-streamlit

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select your repo
4. Set **Main file path**: `app.py`
5. Click **Deploy** — live in ~2 minutes

No environment variables needed. Dataset is included in `data/`.

---

## 📁 Project Structure

```
hr-attrition-streamlit/
│
├── app.py                          # Main entry point — sidebar nav + routing
│
├── pages/
│   ├── home.py                     # Home: KPIs + overview
│   ├── data_overview.py            # Raw data explorer with filters
│   ├── attrition_analysis.py       # Deep attrition EDA
│   ├── demographics.py             # Employee demographics
│   ├── department_insights.py      # Dept-level breakdown
│   ├── prediction.py               # ML model + prediction form
│   └── conclusion.py               # Recommendations + ROI
│
├── utils/
│   ├── data_loader.py              # Cached data loading + feature engineering
│   ├── charts.py                   # 15 reusable Plotly chart functions
│   ├── ml_model.py                 # Random Forest training + prediction
│   └── styles.py                   # Global CSS + UI component helpers
│
├── data/
│   └── HR_Analytics_Data.csv       # IBM HR dataset (1,470 rows × 35 cols)
│
├── requirements.txt
└── README.md
```

---

## 🤖 ML Model Details

| Attribute | Value |
|-----------|-------|
| Algorithm | Random Forest Classifier |
| Trees | 300 estimators |
| Class Handling | `class_weight='balanced'` (handles 16% minority) |
| Train/Test Split | 80/20, stratified |
| Typical Accuracy | ~86% |
| Typical ROC-AUC | ~80% |

**Top predictors:** MonthlyIncome, Age, TotalWorkingYears, OverTime, YearsAtCompany

---

## 📊 Dataset

| Attribute | Detail |
|-----------|--------|
| Source | IBM HR Analytics (public domain) |
| Records | 1,470 employees |
| Features | 35 columns |
| Target | `Attrition` (Yes / No) |
| Missing Values | None |

---

## 🎨 Design System

- **Theme:** Dark corporate (slate + amber + red/green signals)
- **Fonts:** Syne (headings) + DM Sans (body) via Google Fonts
- **Charts:** Plotly interactive — all themed to match
- **Caching:** `@st.cache_data` on data load, `@st.cache_resource` on model training

---

## 👤 Author

**Neha Tiwari** — Data Analyst | Python · SQL · Power BI · Machine Learning

- GitHub: [github.com/tiwarineha73](https://github.com/tiwarineha73)
- LinkedIn: [linkedin.com/in/neha-tiwari](https://linkedin.com/in/neha-tiwari)
- Email: tiwari.neha3111@gmail.com

---

*Part of an end-to-end data analytics portfolio built on real datasets.*
