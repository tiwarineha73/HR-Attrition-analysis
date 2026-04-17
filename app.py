import streamlit as st
import pandas as pd

from home import render as render_home
from data_overview import render as render_data_overview
from attrition_analysis import render as render_attrition
from demographics import render as render_demographics
from department_insights import render as render_department
from prediction import render as render_prediction
from conclusion import render as render_conclusion

st.set_page_config(page_title="HR Analytics", layout="wide")

# Load data
try:
    df = pd.read_csv("HR_Analytics_Data.csv")
except:
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
