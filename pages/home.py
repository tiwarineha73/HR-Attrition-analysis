import streamlit as st
import pandas as pd

def render(df: pd.DataFrame):
    st.title("🏠 HR Attrition Dashboard")

    st.markdown("### Welcome to HR Analytics Dashboard")

    if df.empty:
        st.warning("⚠️ No data loaded")
        return

    st.markdown("### Dataset Preview")
    st.dataframe(df.head())

    st.markdown("### Basic Info")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])
