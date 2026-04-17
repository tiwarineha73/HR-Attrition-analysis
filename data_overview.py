import streamlit as st

def render(df):
    st.title("📊 Data Overview")

    if not df.empty:
        st.write("Shape:", df.shape)
        st.dataframe(df.head())
    else:
        st.warning("No data available")
