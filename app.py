import streamlit as st
import pandas as pd
import sys
import os

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Page config must be first Streamlit command
st.set_page_config(
    page_title="HR Attrition Analytics",
    page_icon="👥",
    layout="wide"
)

  #Hide Streamlit's auto generated 
st.markdown("""
   <style>
           [data-testid="stSidebarNav"]
           [data-testid="stSidebarNavItems"] {display: none !important;}
           section[data-testid="stSidebar"] > div > div > div > div:first-child{
             display: none !important;
             }
    </style>
    """, unsafe_allow_html=True)

# Safe CSS injection (won't crash if utilis is missing)
try:
    from utilis.styles import inject_css
    inject_css()
except Exception:
    pass  # Continue without custom CSS

# Load data safely
@st.cache_data
def load_data():
    possible_paths = [
        os.path.join(BASE_DIR, "HR_Analytics_Data.csv"),
        os.path.join(BASE_DIR, "data", "HR_Analytics_Data.csv"),
        "HR_Analytics_Data.csv",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error("❌ Could not find HR_Analytics_Data.csv. Please make sure it's in the repo root.")
    st.stop()

# Debug line - remove after confirming data loads
st.sidebar.caption(f"✅ Data loaded: {len(df)} rows")

# Import pages safely
def safe_import():
    pages = {}
    
    try:
        from pages.home import render as render_home
        pages["🏠 Home"] = render_home
    except Exception as e:
        pages["🏠 Home"] = lambda df: st.error(f"Home page error: {e}")

    try:
        from pages.data_overview import render as render_data_overview
        pages["📊 Data Overview"] = render_data_overview
    except Exception as e:
        pages["📊 Data Overview"] = lambda df: st.error(f"Data Overview error: {e}")

    try:
        from pages.attrition_analysis import render as render_attrition
        pages["📉 Attrition"] = render_attrition
    except Exception as e:
        pages["📉 Attrition"] = lambda df: st.error(f"Attrition page error: {e}")

    try:
        from pages.demographics import render as render_demographics
        pages["👥 Demographics"] = render_demographics
    except Exception as e:
        pages["👥 Demographics"] = lambda df: st.error(f"Demographics error: {e}")

    try:
        from pages.department_insights import render as render_department
        pages["🏬 Department"] = render_department
    except Exception as e:
        pages["🏬 Department"] = lambda df: st.error(f"Department error: {e}")

    try:
        from pages.prediction import render as render_prediction
        pages["🤖 Prediction"] = render_prediction
    except Exception as e:
        pages["🤖 Prediction"] = lambda df: st.error(f"Prediction error: {e}")

    try:
        from pages.conclusion import render as render_conclusion
        pages["💡 Conclusion"] = render_conclusion
    except Exception as e:
        pages["💡 Conclusion"] = lambda df: st.error(f"Conclusion error: {e}")

    return pages

pages = safe_import()

# Sidebar navigation
st.sidebar.title("📊 HR Analytics")
choice = st.sidebar.selectbox("Navigation", list(pages.keys()))

# Render selected page
try:
    pages[choice](df)
except Exception as e:
    st.error(f"Error rendering page: {e}")
    st.exception(e)  # Shows full traceback to help debug
