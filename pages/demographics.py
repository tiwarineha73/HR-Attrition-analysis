import streamlit as st
import plotly.express as px

def render(df):
    st.title("👥 Demographics")

    if "Age" in df.columns:
        fig = px.histogram(df, x="Age")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Age column not found")
