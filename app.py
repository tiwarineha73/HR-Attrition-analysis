"""
app.py — Main entry point for the HR Attrition Analytics Streamlit App.
Run with: streamlit run app.py
"""

import streamlit as st

# ── Page config MUST be first Streamlit call ───────────────────────────────────
st.set_page_config(
    page_title="HR Attrition Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# ── Utils imports ──────────────────────────────────────────────────────────────
from utils.styles import inject_css
from utils.data_loader import load_data

# ── FIXED: Page imports (REMOVED 'pages.') ─────────────────────────────────────
from home import render as render_home
from data_overview import render as render_data_overview
from attrition_analysis import render as render_attrition
from demographics import render as render_demographics
from department_insights import render as render_department
from prediction import render as render_prediction
from conclusion import render as render_conclusion

# ── Inject global CSS ──────────────────────────────────────────────────────────
inject_css()

# ── Load data (cached) ─────────────────────────────────────────────────────────
df = load_data()

# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom:1rem">
        <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#f5a623">
            🏢 HR Analytics
        </div>
        <div style="font-size:0.75rem; color:#8b90a7; margin-top:3px">IBM Dataset · 1,470 Employees</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home": "home",
        "📋  Data Overview": "data_overview",
        "📉  Attrition Analysis": "attrition",
        "👥  Employee Demographics": "demographics",
        "🏬  Department Insights": "department",
        "🤖  Attrition Predictor": "prediction",
        "💡  Conclusions": "conclusion",
    }

    selection = st.radio(
        "Navigation",
        list(pages.keys()),
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem; color:#8b90a7; border-top:1px solid rgba(255,255,255,0.06); padding-top:1rem">
        <b style="color:#f0f2f8">Neha Tiwari</b><br>
        Data Analyst · Python · SQL · ML<br>
        <a href="https://github.com/tiwarineha73" style="color:#f5a623; text-decoration:none">
            github.com/tiwarineha73
        </a>
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ─────────────────────────────────────────────────────────────
page_key = pages[selection]

if page_key == "home":
    render_home(df)
elif page_key == "data_overview":
    render_data_overview(df)
elif page_key == "attrition":
    render_attrition(df)
elif page_key == "demographics":
    render_demographics(df)
elif page_key == "department":
    render_department(df)
elif page_key == "prediction":
    render_prediction(df)
elif page_key == "conclusion":
    render_conclusion(df)
