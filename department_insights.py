import streamlit as st
import plotly.express as px

def render(df):
    st.title("🏬 Department Insights")

    if "Department" in df.columns:
        fig = px.bar(df["Department"].value_counts())
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Department column not found")
