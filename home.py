import streamlit as st

def render(df):
    st.title("🏠 HR Attrition Dashboard")

    st.markdown("### Welcome to HR Analytics Dashboard")

    st.write("Dataset Preview:")
    st.dataframe(df.head())

    st.write("Basic Info:")
    st.write(f"Total Rows: {df.shape[0]}")
    st.write(f"Total Columns: {df.shape[1]}")
