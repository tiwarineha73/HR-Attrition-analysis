import streamlit as st
import pandas as pd
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from pages.home import render as render_home
from pages.data_overview import render as render_data_overview
from pages.attrition_analysis import render as render_attrition
from pages.demographics import render as render_demographics
from pages.department_insights import render as render_department
from pages.prediction import render as render_prediction
from pages.conclusion import render as render_conclusion
from utilis.styles import inject_css

st.set_page_config(page_title="HR Analytics", layout="wide")
inject_css()

# Load data safely
try:
    file_path = os.path.join(os.path.dirname(__file__), "HR_Analytics_Data.csv")
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error loading data: {e}")
    df = pd.DataFrame()

pages = {
    "🏠 Home": render_home,
    "📊 Data Overview": render_data_overview,
    "📉 Attrition": render_attrition,
    "👥 Demographics": render_demographics,
    "🏬 Department": render_department,
    "🤖 Prediction": render_prediction,
    "💡 Conclusion": render_conclusion,
}

choice = st.sidebar.selectbox("Navigation", list(pages.keys()))
pages[choice](df)
