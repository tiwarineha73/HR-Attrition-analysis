"""
styles.py — Global CSS injection for the Streamlit app.
Corporate dark-slate + amber accent theme.
"""

THEME_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Root variables ───────────────────────────────────────────────────────── */
:root {
    --bg-primary:    #0f1117;
    --bg-card:       #1a1d2e;
    --bg-card2:      #12152a;
    --accent:        #f5a623;
    --accent2:       #e05252;
    --accent3:       #3ecf8e;
    --text-primary:  #f0f2f8;
    --text-muted:    #8b90a7;
    --border:        rgba(255,255,255,0.06);
    --shadow:        0 4px 24px rgba(0,0,0,0.4);
    --radius:        14px;
}

/* ── App background ───────────────────────────────────────────────────────── */
.stApp {
    background-color: var(--bg-primary);
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-card2) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem;
    padding: 8px 0;
    cursor: pointer;
}

/* ── Hide default Streamlit chrome ────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── KPI Cards ────────────────────────────────────────────────────────────── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    margin: 0.3rem 0;
}
.kpi-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-delta {
    font-size: 0.78rem;
    color: var(--accent3);
    margin-top: 0.3rem;
}

/* ── Section headers ──────────────────────────────────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 1.6rem 0 0.4rem;
    letter-spacing: -0.01em;
}
.section-subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 1.2rem;
}
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0 1.6rem;
}

/* ── Insight cards ────────────────────────────────────────────────────────── */
.insight-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text-primary);
}
.insight-card.critical { border-left-color: var(--accent2); }
.insight-card.positive { border-left-color: var(--accent3); }

/* ── Badge ────────────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge-red   { background: rgba(224,82,82,0.15); color: #e05252; }
.badge-green { background: rgba(62,207,142,0.15); color: #3ecf8e; }
.badge-amber { background: rgba(245,166,35,0.15); color: #f5a623; }

/* ── Page hero ────────────────────────────────────────────────────────────── */
.page-hero {
    background: linear-gradient(135deg, #1a1d2e 0%, #0f1117 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.page-hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(245,166,35,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.page-hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.4rem;
}
.page-hero p {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin: 0;
}

/* ── Streamlit widget overrides ───────────────────────────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSlider > div > div { color: var(--accent) !important; }

/* ── Plotly chart containers ──────────────────────────────────────────────── */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* ── Prediction result ────────────────────────────────────────────────────── */
.pred-result {
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1rem;
    font-family: 'Syne', sans-serif;
}
.pred-result.will-leave {
    background: rgba(224,82,82,0.1);
    border: 2px solid rgba(224,82,82,0.4);
}
.pred-result.will-stay {
    background: rgba(62,207,142,0.1);
    border: 2px solid rgba(62,207,142,0.4);
}
.pred-result .pred-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.pred-result .pred-label { font-size: 1.6rem; font-weight: 800; margin: 0.3rem 0; }
.pred-result .pred-prob { font-size: 0.9rem; color: var(--text-muted); }

/* ── Table overrides ──────────────────────────────────────────────────────── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── Expander ─────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def kpi_card(value, label, delta=None, color="amber"):
    color_map = {"amber": "#f5a623", "red": "#e05252", "green": "#3ecf8e", "blue": "#4da6ff"}
    hex_color = color_map.get(color, "#f5a623")
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{hex_color}">{value}</div>
        {delta_html}
    </div>
    """


def insight_card(text, variant="default"):
    css_class = {"critical": "insight-card critical", "positive": "insight-card positive"}.get(
        variant, "insight-card"
    )
    return f'<div class="{css_class}">{text}</div>'


def page_hero(title, subtitle, emoji=""):
    import streamlit as st
    st.markdown(
        f"""
        <div class="page-hero">
            <h1>{emoji} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=""):
    import streamlit as st
    sub = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<p class="section-title">{title}</p>{sub}<hr class="section-divider">',
        unsafe_allow_html=True,
    )
