from download_models import download_models
download_models()
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="Intelligent Agri Advisory System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── 1. STYLES ONLY ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Nunito:wght@400;600;700;800&display=swap');

* { font-family: 'Nunito', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: linear-gradient(160deg, #052e16 0%, #14532d 35%, #166534 65%, #15803d 100%);
    min-height: 100vh;
}

/* hide sidebar, menu, footer, header */
#MainMenu, footer, .stDeployButton, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* hide streamlit top padding */
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; }
.stMainBlockContainer { padding-top: 0 !important; }

/* remove gap between streamlit elements */
div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }

/* ── decorative background circles ── */
.bg-circle-1 {
    position: fixed; top: -120px; right: -120px;
    width: 420px; height: 420px; border-radius: 50%;
    background: rgba(34,197,94,0.08); pointer-events: none; z-index: 0;
}
.bg-circle-2 {
    position: fixed; bottom: -80px; left: -80px;
    width: 300px; height: 300px; border-radius: 50%;
    background: rgba(74,222,128,0.06); pointer-events: none; z-index: 0;
}
.bg-circle-3 {
    position: fixed; top: 40%; left: 50%;
    width: 500px; height: 500px; border-radius: 50%;
    background: rgba(21,128,61,0.12); pointer-events: none; z-index: 0;
    transform: translate(-50%, -50%);
}

/* ── hero section ── */
.hero-wrap {
    text-align: center;
    padding: 60px 20px 10px 20px;
    position: relative; z-index: 1;
    animation: fadeDown 0.7s ease-out both;
}
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.logo-ring {
    width: 96px; height: 96px; border-radius: 50%;
    background: rgba(255,255,255,0.12);
    border: 2px solid rgba(255,255,255,0.25);
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 3rem; margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(74,222,128,0.2);
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 3.2rem; font-weight: 900;
    color: #ffffff;
    letter-spacing: -1px;
    line-height: 1.1;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}
.hero-title span { color: #86efac; }

.hero-sub {
    font-size: 1.15rem; color: rgba(255,255,255,0.75);
    margin: 14px auto 0 auto; max-width: 540px; line-height: 1.7;
    font-weight: 600;
}

/* ── pill badges ── */
.badge-row {
    display: flex; flex-wrap: wrap; gap: 10px;
    justify-content: center; margin: 24px 0 0 0;
}
.badge {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.9);
    padding: 6px 16px; border-radius: 30px;
    font-size: 0.82rem; font-weight: 700;
    letter-spacing: 0.3px;
}

/* ── divider ── */
.divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #4ade80, #86efac);
    border-radius: 2px; margin: 36px auto 12px auto;
}
.choose-label {
    text-align: center; color: rgba(255,255,255,0.5);
    font-size: 0.8rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 28px;
}

/* ── cards wrapper ── */
.cards-wrapper {
    display: flex; gap: 28px; justify-content: center;
    flex-wrap: wrap; padding: 0 24px 20px 24px;
    position: relative; z-index: 1;
}

/* ── feature card ── */
.feature-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 28px;
    padding: 40px 36px 36px 36px;
    width: 340px; min-width: 280px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
    animation: fadeUp 0.7s ease-out both;
    position: relative; overflow: hidden;
}
.feature-card:nth-child(1) { animation-delay: 0.15s; }
.feature-card:nth-child(2) { animation-delay: 0.28s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(32px); }
    to   { opacity: 1; transform: translateY(0); }
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.35);
    background: rgba(255,255,255,0.13);
}

.feature-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    border-radius: 28px 28px 0 0;
}
.card-disease::before { background: linear-gradient(90deg, #4ade80, #22c55e); }
.card-yield::before   { background: linear-gradient(90deg, #fbbf24, #f59e0b); }

.card-icon {
    font-size: 3.4rem; margin-bottom: 20px;
    display: block;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
}
.card-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.5rem; font-weight: 800;
    color: #ffffff; margin-bottom: 10px;
    line-height: 1.2;
}
.card-desc {
    font-size: 0.92rem; color: rgba(255,255,255,0.65);
    line-height: 1.7; margin-bottom: 24px;
    font-weight: 600;
}

.card-features { list-style: none; margin-bottom: 0px; }
.card-features li {
    font-size: 0.85rem; color: rgba(255,255,255,0.75);
    padding: 5px 0; display: flex; align-items: center; gap: 8px;
    font-weight: 600;
}
.card-features li::before {
    content: '✓';
    background: rgba(74,222,128,0.2);
    color: #4ade80;
    border-radius: 50%;
    width: 20px; height: 20px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 800; flex-shrink: 0;
}
.card-yield .card-features li::before {
    background: rgba(251,191,36,0.2);
    color: #fbbf24;
}

/* ── stats strip ── */
.stats-strip {
    display: flex; gap: 0; justify-content: center; flex-wrap: wrap;
    margin: 36px auto 0 auto;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; max-width: 720px; overflow: hidden;
    position: relative; z-index: 1;
    animation: fadeUp 0.7s 0.4s ease-out both;
}
.stat-item {
    flex: 1; min-width: 130px; padding: 22px 16px;
    text-align: center; border-right: 1px solid rgba(255,255,255,0.08);
}
.stat-item:last-child { border-right: none; }
.stat-num {
    font-family: 'Poppins', sans-serif;
    font-size: 1.8rem; font-weight: 900; color: #4ade80;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.72rem; color: rgba(255,255,255,0.5);
    font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; margin-top: 4px;
}

/* ── footer ── */
.home-footer {
    text-align: center; padding: 32px 20px 40px 20px;
    color: rgba(255,255,255,0.3);
    font-size: 0.78rem; font-weight: 600;
    position: relative; z-index: 1;
    animation: fadeUp 0.7s 0.5s ease-out both;
}
.home-footer a { color: rgba(255,255,255,0.45); text-decoration: none; }

/* ── streamlit button overrides ── */
div.stButton > button {
    width: 100% !important;
    padding: 16px 0 !important;
    border-radius: 14px !important;
    border: none !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    color: white !important;
    margin-top: 20px !important;
}

/* disease button (col index 2 = second column) */
div[data-testid="column"]:nth-child(2) div.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    box-shadow: 0 6px 20px rgba(22,163,74,0.45) !important;
}
div[data-testid="column"]:nth-child(2) div.stButton > button:hover {
    box-shadow: 0 8px 28px rgba(22,163,74,0.65) !important;
    transform: scale(1.02) !important;
}

/* yield button (col index 4 = fourth column) */
div[data-testid="column"]:nth-child(4) div.stButton > button {
    background: linear-gradient(135deg, #d97706, #b45309) !important;
    box-shadow: 0 6px 20px rgba(217,119,6,0.45) !important;
}
div[data-testid="column"]:nth-child(4) div.stButton > button:hover {
    box-shadow: 0 8px 28px rgba(217,119,6,0.65) !important;
    transform: scale(1.02) !important;
}
</style>
""", unsafe_allow_html=True)


# ── 2. BACKGROUND BLOBS ─────────────────────────────────────────────────────
st.markdown("""
<div class="bg-circle-1"></div>
<div class="bg-circle-2"></div>
<div class="bg-circle-3"></div>
""", unsafe_allow_html=True)


# ── 3. HERO ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="logo-ring">🌾</div>
    <div class="hero-title">Intelligent Agri<br><span>Advisory System</span></div>
    <div class="hero-sub">
        AI-powered tools built for Indian farmers — detect diseases early
        and predict crop yields with confidence.
    </div>
    <div class="badge-row">
        <span class="badge">Made for Indian Farmers</span>
        <span class="badge">🤖 EfficientNetB3 AI</span>
        <span class="badge">🎯 97%+ Accuracy</span>
        <span class="badge">🌐 Free to Use</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── 4. DIVIDER + CARDS ──────────────────────────────────────────────────────
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;800;900&family=Nunito:wght@400;600;700;800&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Nunito', sans-serif; }
body { background: transparent; }

.divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #4ade80, #86efac);
    border-radius: 2px; margin: 10px auto 12px auto;
}
.choose-label {
    text-align: center; color: rgba(255,255,255,0.5);
    font-size: 0.8rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 28px;
}
.cards-wrapper {
    display: flex; gap: 28px; justify-content: center;
    flex-wrap: wrap; padding: 0 24px 20px 24px;
}
.feature-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 28px;
    padding: 40px 36px 36px 36px;
    width: 340px; min-width: 280px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
    position: relative; overflow: hidden;
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.35);
    background: rgba(255,255,255,0.13);
}
.feature-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    border-radius: 28px 28px 0 0;
}
.card-disease::before { background: linear-gradient(90deg, #4ade80, #22c55e); }
.card-yield::before   { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.card-icon { font-size: 3.4rem; margin-bottom: 20px; display: block; }
.card-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.5rem; font-weight: 800;
    color: #ffffff; margin-bottom: 10px; line-height: 1.2;
}
.card-desc {
    font-size: 0.92rem; color: rgba(255,255,255,0.65);
    line-height: 1.7; margin-bottom: 24px; font-weight: 600;
}
.card-features { list-style: none; margin-bottom: 0; }
.card-features li {
    font-size: 0.85rem; color: rgba(255,255,255,0.75);
    padding: 5px 0; display: flex; align-items: center; gap: 8px; font-weight: 600;
}
.card-features li::before {
    content: '✓';
    background: rgba(74,222,128,0.2); color: #4ade80;
    border-radius: 50%; width: 20px; height: 20px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 800; flex-shrink: 0;
}
.card-yield .card-features li::before {
    background: rgba(251,191,36,0.2); color: #fbbf24;
}
</style>
</head>
<body>
<div class="divider"></div>
<div class="choose-label">Choose a tool to get started</div>
<div class="cards-wrapper">
    <div class="feature-card card-disease">
        <span class="card-icon">🔬</span>
        <div class="card-title">Plant Disease<br>Detection</div>
        <div class="card-desc">Upload a photo of your crop leaf and get an instant AI diagnosis with pesticide recommendations.</div>
        <ul class="card-features">
            <li>Detects 38 diseases across 14 crops</li>
            <li>Top 5 pesticide recommendations</li>
            <li>Severity rating & prevention tips</li>
            <li>Download full diagnosis report</li>
        </ul>
    </div>
    <div class="feature-card card-yield">
        <span class="card-icon">📊</span>
        <div class="card-title">Crop Yield<br>Prediction</div>
        <div class="card-desc">Enter your field details — soil, weather, crop type — and get an accurate yield forecast to plan your harvest.</div>
        <ul class="card-features">
            <li>Supports major Indian crops</li>
            <li>Uses soil, rainfall & area inputs</li>
            <li>Season-wise smart predictions</li>
            <li>Easy-to-read yield estimate</li>
        </ul>
    </div>
</div>
</body>
</html>
""", height=520, scrolling=False)


# ── 5. NAVIGATION BUTTONS (below cards) ─────────────────────────────────────
col_gap1, col1, col_mid, col2, col_gap2 = st.columns([1.2, 2, 0.4, 2, 1.2])

with col1:
    if st.button("🔬  Detect Plant Disease", key="btn_disease", use_container_width=True):
        st.switch_page("pages/app.py")

with col2:
    if st.button("📊  Predict Crop Yield", key="btn_yield", use_container_width=True):
        st.switch_page("pages/yield_app.py")


# ── 6. STATS + FOOTER ───────────────────────────────────────────────────────
st.markdown("""
<div class="stats-strip">
    <div class="stat-item">
        <div class="stat-num">38</div>
        <div class="stat-lbl">Diseases Detected</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">14</div>
        <div class="stat-lbl">Crops Supported</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">97%+</div>
        <div class="stat-lbl">AI Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">Free</div>
        <div class="stat-lbl">Always Free</div>
    </div>
</div>

<div class="home-footer">
    🌿 Intelligent Agri Advisory System &nbsp;
    <br>Made by: <strong style="color:rgba(255,255,255,0.5)">Shubhankar &nbsp|&nbsp  Himanshu &nbsp|&nbsp Ritik </strong>
    <br><br>
    Built for farmers of India &nbsp; For educational use only — always consult your local agronomist.
</div>
""", unsafe_allow_html=True)