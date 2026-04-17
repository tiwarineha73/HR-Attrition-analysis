import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

st.set_page_config(
    page_title="HR Dashboard - Full Insights",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide auto-generated Streamlit top nav
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}

        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
            text-align: center;
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #e53935;
            margin: 0;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #555;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .metric-sub {
            font-size: 1rem;
            color: #333;
            font-weight: 600;
        }
        .section-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
            height: 100%;
        }
        .header-bar {
            background: white;
            border-radius: 12px;
            padding: 16px 24px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            margin-bottom: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    for path in [
        os.path.join(BASE_DIR, "HR_Analytics_Data.csv"),
        "HR_Analytics_Data.csv",
    ]:
        if os.path.exists(path):
            df = pd.read_csv(path, sep=None, engine='python')
            return df
    return None

df = load_data()

if df is None:
    st.error("❌ HR_Analytics_Data.csv not found!")
    st.stop()

# ── KPI Calculations ──────────────────────────────────────────
total_emp       = len(df)
male            = (df['Gender'] == 'Male').sum()
female          = (df['Gender'] == 'Female').sum()
male_pct        = round(male / total_emp * 100)
female_pct      = round(female / total_emp * 100)

# Promotion: employees with YearsSinceLastPromotion == 0 => due
due_promo       = (df['YearsSinceLastPromotion'] == 0).sum()
not_due_promo   = total_emp - due_promo
due_pct         = round(due_promo / total_emp * 100, 2)
not_due_pct     = round(not_due_promo / total_emp * 100, 2)

# Retrenchment: Attrition == Yes
retrenched      = (df['Attrition'] == 'Yes').sum()
active          = (df['Attrition'] == 'No').sum()
retrenched_pct  = round(retrenched / total_emp * 100, 1)
active_pct      = round(active / total_emp * 100, 1)

# Service years
service_years   = df['YearsAtCompany'].value_counts().sort_index()
top_service     = service_years.nlargest(10).sort_values(ascending=True)

# Job level
job_level_counts = df['JobLevel'].value_counts().sort_index()

# Distance from home
def dist_category(d):
    if d <= 5:   return 'Very Close'
    elif d <= 15: return 'Close'
    else:         return 'Very Far'

df['DistCategory'] = df['DistanceFromHome'].apply(dist_category)
dist_counts = df['DistCategory'].value_counts()

# ── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.markdown("## 📊 HR Analytics")
page = st.sidebar.selectbox("Navigation", [
    "🏠 Dashboard",
    "📊 Data Overview",
    "📉 Attrition Analysis",
    "👥 Demographics",
    "🏬 Department Insights",
    "💡 Conclusion"
])

# ── DASHBOARD PAGE ────────────────────────────────────────────
if page == "🏠 Dashboard":

    # Header
    st.markdown("""
        <div style='background:white; border-radius:12px; padding:16px 24px;
                    box-shadow:2px 2px 10px rgba(0,0,0,0.08); margin-bottom:16px;
                    display:flex; align-items:center; gap:16px;'>
            <div style='background:#e53935; width:18px; height:18px;
                        border-radius:50%; display:inline-block;'></div>
            <div>
                <span style='font-size:1.4rem; font-weight:800;'>HR Dashboard</span><br>
                <span style='color:#888; font-size:0.85rem;'>Full insights</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Top KPIs
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Total Employees</div>
                <div class='metric-value'>{total_emp:,}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>👤 Male</div>
                <div class='metric-value'>{male:,}</div>
                <div class='metric-sub'>{male_pct}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>👩 Female</div>
                <div class='metric-value'>{female:,}</div>
                <div class='metric-sub'>{female_pct}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Active Workers</div>
                <div class='metric-value'>{active:,}</div>
                <div class='metric-sub'>{active_pct}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Promotion | Service Years | Retrenchment | Distance
    col1, col2, col3, col4 = st.columns([1, 2, 1, 2])

    with col1:
        st.markdown(f"""
            <div class='section-card'>
                <div class='metric-label'>Not Due for Promotion</div>
                <div class='metric-value'>{not_due_promo:,}</div>
                <div class='metric-sub'>{not_due_pct}%</div>
                <hr>
                <div class='metric-label'>Due for Promotion</div>
                <div class='metric-value'>{due_promo:,}</div>
                <div class='metric-sub'>{due_pct}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        fig_service = px.bar(
            x=top_service.values,
            y=[f"{y} years" for y in top_service.index],
            orientation='h',
            title="Service Years",
            color_discrete_sequence=["#e53935"],
            text=top_service.values
        )
        fig_service.update_layout(
            height=320, margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis_title="", yaxis_title="",
            showlegend=False
        )
        fig_service.update_traces(textposition='outside')
        st.plotly_chart(fig_service, use_container_width=True)

    with col3:
        st.markdown(f"""
            <div class='section-card'>
                <div class='metric-label'>Next Retrenchment</div>
                <div class='metric-value'>{retrenched:,}</div>
                <div class='metric-sub'>{retrenched_pct}%</div>
                <hr>
                <div class='metric-label'>Active Workers</div>
                <div class='metric-value'>{active:,}</div>
                <div class='metric-sub'>{active_pct}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        fig_dist = px.pie(
            names=dist_counts.index,
            values=dist_counts.values,
            title="Distance from Office",
            hole=0.5,
            color_discrete_sequence=["#FFA726", "#FFCC80", "#e53935"]
        )
        fig_dist.update_layout(
            height=320, margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: Job Level
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig_job = px.bar(
            x=[f"Level {l}" for l in job_level_counts.index],
            y=job_level_counts.values,
            title="Job Levels View",
            color_discrete_sequence=["#FFA726"],
            text=job_level_counts.values
        )
        fig_job.update_layout(
            height=280, margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis_title="", yaxis_title=""
        )
        fig_job.update_traces(textposition='outside')
        st.plotly_chart(fig_job, use_container_width=True)

    with col_b:
        dept_counts = df['Department'].value_counts()
        fig_dept = px.pie(
            names=dept_counts.index,
            values=dept_counts.values,
            title="By Department",
            color_discrete_sequence=["#e53935", "#FFA726", "#FFCC80"]
        )
        fig_dept.update_layout(
            height=280, margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_dept, use_container_width=True)

# ── DATA OVERVIEW PAGE ────────────────────────────────────────
elif page == "📊 Data Overview":
    st.title("📊 Data Overview")
    st.markdown(f"**Total Rows:** {len(df)} | **Total Columns:** {len(df.columns)}")
    st.dataframe(df.head(20), use_container_width=True)
    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

# ── ATTRITION ANALYSIS PAGE ───────────────────────────────────
elif page == "📉 Attrition Analysis":
    st.title("📉 Attrition Analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Attrition", retrenched)
    c2.metric("Attrition Rate", f"{retrenched_pct}%")
    c3.metric("Active Employees", active)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='Attrition', title='Attrition Distribution',
                     color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        dept_att = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
        fig2 = px.bar(dept_att, x='Department', y='Count', color='Attrition',
                      title='Attrition by Department',
                      color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        age_att = df.groupby(['Age', 'Attrition']).size().reset_index(name='Count')
        fig3 = px.line(age_att, x='Age', y='Count', color='Attrition',
                       title='Attrition by Age',
                       color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        job_att = df.groupby(['JobRole', 'Attrition']).size().reset_index(name='Count')
        fig4 = px.bar(job_att, x='Count', y='JobRole', color='Attrition',
                      orientation='h', title='Attrition by Job Role',
                      color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig4, use_container_width=True)

# ── DEMOGRAPHICS PAGE ─────────────────────────────────────────
elif page == "👥 Demographics":
    st.title("👥 Demographics")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='Gender', title='Gender Distribution',
                     color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.histogram(df, x='Age', color='Gender', title='Age Distribution',
                            color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.pie(df, names='MaritalStatus', title='Marital Status',
                      color_discrete_sequence=["#e53935", "#FFA726", "#1565C0"])
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        fig4 = px.pie(df, names='EducationField', title='Education Field',
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig4, use_container_width=True)

# ── DEPARTMENT INSIGHTS PAGE ──────────────────────────────────
elif page == "🏬 Department Insights":
    st.title("🏬 Department Insights")
    col1, col2 = st.columns(2)
    with col1:
        dept = df['Department'].value_counts().reset_index()
        dept.columns = ['Department', 'Count']
        fig = px.bar(dept, x='Department', y='Count', title='Employees by Department',
                     color_discrete_sequence=["#e53935"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.box(df, x='Department', y='MonthlyIncome', title='Salary by Department',
                      color='Department',
                      color_discrete_sequence=["#e53935", "#FFA726", "#1565C0"])
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.histogram(df, x='JobRole', color='Department',
                            title='Job Roles by Department')
        fig3.update_xaxes(tickangle=45)
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        overtime = df.groupby(['Department', 'OverTime']).size().reset_index(name='Count')
        fig4 = px.bar(overtime, x='Department', y='Count', color='OverTime',
                      title='Overtime by Department',
                      color_discrete_sequence=["#1565C0", "#e53935"])
        st.plotly_chart(fig4, use_container_width=True)

# ── CONCLUSION PAGE ───────────────────────────────────────────
elif page == "💡 Conclusion":
    st.title("💡 Key Findings & Conclusion")
    st.markdown(f"""
    ### 📌 Summary

    - **Total Employees:** {total_emp:,}
    - **Male:** {male:,} ({male_pct}%) | **Female:** {female:,} ({female_pct}%)
    - **Attrition Rate:** {retrenched_pct}% ({retrenched:,} employees left)
    - **Active Workers:** {active:,} ({active_pct}%)
    - **Due for Promotion:** {due_promo:,} ({due_pct}%)

    ### 🔍 Key Insights
    - Most employees have been with the company for **10 years**
    - Majority of employees are at **Job Level 1 and 2**
    - **63.95%** of employees live very close to the office
    - Attrition is highest in the **Sales** department

    ### ✅ Recommendations
    - Focus retention efforts on **Sales** department
    - Review promotion policies — only **{due_pct}%** are due for promotion
    - Support employees at **Level 1** with career growth opportunities
    """)
