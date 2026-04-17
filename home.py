import streamlit as st
import pandas as pd

def render(df):
    st.markdown("## 🏢 HR Dashboard")

    if df.empty:
        st.warning("No data loaded")
        return

    # ── KPIs ─────────────────────────────
    total = len(df)
    male = df[df["Gender"] == "Male"].shape[0]
    female = df[df["Gender"] == "Female"].shape[0]
    active = df[df["Attrition"] == "No"].shape[0]
    attrition = df[df["Attrition"] == "Yes"].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
        <div class="card">
            <h4>Total Employees</h4>
            <h2>{total}</h2>
        </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
        <div class="card">
            <h4>Male</h4>
            <h2>{male}</h2>
        </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
        <div class="card">
            <h4>Female</h4>
            <h2>{female}</h2>
        </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
        <div class="card">
            <h4>Attrition</h4>
            <h2>{attrition}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Second row ───────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="card">
                <h4>Active Employees</h4>
                <h2>{active}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card">
            import plotly.express as px

st.markdown("### 📊 Attrition Overview")

fig = px.pie(df, names="Attrition", hole=0.5)
st.plotly_chart(fig, use_container_width=True)
                <h4>Attrition Rate</h4>
                <h2>{round(attrition/total*100,2)}%</h2>
            </div>
        """, unsafe_allow_html=True)
