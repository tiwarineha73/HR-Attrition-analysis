# pages package
import streamlit as st
import plotly.express as px

def render(df):
    st.title("📉 Attrition Analysis")

    # Attrition count
    attrition_count = df['Attrition'].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Attrition Distribution")
        fig = px.pie(
            values=attrition_count.values,
            names=attrition_count.index,
            title="Employee Attrition"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Attrition by Department")
        dept_attrition = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
        fig2 = px.bar(
            dept_attrition,
            x='Department',
            y='Count',
            color='Attrition',
            barmode='group'
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Monthly Income vs Attrition")
    fig3 = px.box(
        df,
        x='Attrition',
        y='MonthlyIncome',
        color='Attrition'
    )
    st.plotly_chart(fig3, use_container_width=True)
