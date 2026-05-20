import streamlit as st
import sys
import os

# ── make root-level modules importable from pages/ ──
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yield_predict import predict_yield, get_recommendations

st.set_page_config(
    page_title="🌾 Crop Yield Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Nunito:wght@400;600;700&display=swap');

    * { font-family: 'Nunito', sans-serif; }

    .stApp {
        background: linear-gradient(135deg,#fffbeb 0%,#fef3c7 30%,#fffbeb 60%,#fefce8 100%);
        background-attachment: fixed;
    }
    #MainMenu, footer, .stDeployButton, header { visibility: hidden; }

    .yield-hero {
        background: linear-gradient(135deg,#78350f 0%,#92400e 40%,#b45309 70%,#d97706 100%);
        border-radius: 20px; padding: 38px 30px; text-align: center;
        margin-bottom: 28px; box-shadow: 0 10px 40px rgba(120,53,15,0.3);
    }
    .yield-hero-title {
        font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 800;
        color: white; margin: 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .yield-hero-sub { font-size: 1rem; color: rgba(255,255,255,0.85); margin: 8px 0 0 0; }
    .badge {
        background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
        color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.82rem;
        font-weight: 600; display: inline-block; margin: 4px;
    }

    .section-card {
        background: white; border-radius: 20px; padding: 28px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); margin-bottom: 20px;
    }
    .section-header {
        font-family: 'Poppins', sans-serif; font-size: 1.05rem; font-weight: 700;
        color: #78350f; margin: 0 0 18px 0; padding-bottom: 10px;
        border-bottom: 2px solid #fde68a; display: flex; align-items: center; gap: 8px;
    }

    .stSelectbox label, .stNumberInput label, .stSlider label {
        font-weight: 700 !important; color: #374151 !important; font-size: 0.9rem !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg,#d97706,#b45309) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; font-family: 'Poppins',sans-serif !important;
        font-size: 1.1rem !important; font-weight: 700 !important;
        padding: 14px 0 !important;
        box-shadow: 0 6px 20px rgba(217,119,6,0.4) !important;
        transition: all 0.2s !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 30px rgba(217,119,6,0.6) !important;
        transform: translateY(-2px) !important;
    }
    div.stButton > button[kind="secondary"] {
        background: white !important; color: #374151 !important;
        border: 2px solid #d1d5db !important; border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .result-card {
        background: linear-gradient(135deg,#78350f,#b45309);
        border-radius: 24px; padding: 40px 30px; text-align: center;
        color: white; box-shadow: 0 8px 40px rgba(120,53,15,0.35);
        animation: popIn 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    }
    @keyframes popIn {
        from { opacity:0; transform: scale(0.85); }
        to   { opacity:1; transform: scale(1); }
    }
    .result-number {
        font-family: 'Poppins',sans-serif; font-size: 4rem; font-weight: 900;
        color: #fde68a; line-height: 1; margin: 12px 0 4px 0;
        text-shadow: 0 2px 16px rgba(0,0,0,0.3);
    }
    .result-unit { font-size: 1.1rem; color: rgba(255,255,255,0.8); font-weight: 600; }
    .result-label { font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-top: 6px; font-weight: 600; }

    .insight-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px; }
    .insight-chip {
        flex:1; min-width: 110px; background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2); border-radius: 12px;
        padding: 14px 10px; text-align: center;
    }
    .insight-val { font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:800; color:#fde68a; }
    .insight-lbl { font-size:0.72rem; color:rgba(255,255,255,0.6); font-weight:700; text-transform:uppercase; margin-top:3px; }

    .rating-bar-bg { background:#fef3c7; border-radius:10px; height:12px; overflow:hidden; margin:8px 0 4px 0; }
    .rating-bar-fill { height:100%; border-radius:10px; transition:width 1.2s ease-out; }

    .tip-card {
        background: linear-gradient(135deg,#fffbeb,#fef3c7);
        border-radius: 12px; padding: 14px; margin-bottom: 10px;
        border-left: 4px solid #f59e0b;
    }
    .tip-title { font-weight: 700; color: #78350f; margin-bottom: 4px; font-size:0.9rem; }
    .tip-body { color: #374151; font-size: 0.85rem; line-height: 1.6; }

    .advice-card {
        background: #eff6ff; border-left: 4px solid #2563eb;
        border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;
        font-size: 0.85rem; color: #1e3a8a; font-weight: 600;
    }

    .sidebar-card {
        background: white; border-radius: 14px; padding: 16px;
        margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .sidebar-title {
        font-family:'Poppins',sans-serif; font-weight:700; color:#78350f;
        margin-bottom:8px; font-size:0.95rem;
    }

    .await-box {
        background:white; border-radius:20px; padding:50px 30px;
        text-align:center; box-shadow:0 4px 20px rgba(0,0,0,0.06);
        border: 2px dashed #fde68a;
    }

    .stSelectbox > div > div { border-radius: 10px !important; border-color: #fde68a !important; }
    .stNumberInput > div > div > input { border-radius: 10px !important; }
    div[data-baseweb="select"] { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
CROPS = [
    "Arecanut", "Arhar/Tur", "Bajra", "Banana", "Barley",
    "Blackpepper", "Cardamom", "Cashewnut", "Castor seed",
    "Coconut", "Coriander", "Cotton(lint)", "Cowpea(Lobia)",
    "Dry chillies", "Garlic", "Ginger", "Gram", "Groundnut",
    "Guar seed", "Horse-gram", "Jowar", "Jute", "Khesari",
    "Linseed", "Maize", "Masoor", "Mesta", "Moong(Green Gram)",
    "Moth", "Niger seed", "Oilseeds total", "Onion",
    "Other  Rabi pulses", "Peas & beans (Pulses)",
    "Potato", "Ragi", "Rapeseed &Mustard", "Rice",
    "Safflower", "Sannhamp", "Sesamum", "Small millets",
    "Soyabean", "Sugarcane", "Sunflower", "Sweet potato",
    "Tapioca", "Tobacco", "Turmeric", "Urad", "Wheat",
]

SEASONS = ["Kharif", "Rabi", "Whole Year", "Autumn", "Summer", "Winter"]

STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

STATE_RAINFALL_DEFAULTS = {
    "Andaman and Nicobar Islands": 3000, "Andhra Pradesh": 930,
    "Assam": 2800, "Bihar": 1200, "Chhattisgarh": 1400,
    "Goa": 3000, "Gujarat": 800, "Haryana": 600,
    "Himachal Pradesh": 1600, "Jammu and Kashmir": 1100,
    "Jharkhand": 1400, "Karnataka": 1250, "Kerala": 3000,
    "Madhya Pradesh": 1050, "Maharashtra": 1150, "Manipur": 1500,
    "Meghalaya": 2800, "Mizoram": 2500, "Nagaland": 1800,
    "Odisha": 1500, "Punjab": 650, "Rajasthan": 330,
    "Sikkim": 3500, "Tamil Nadu": 1000, "Telangana": 950,
    "Tripura": 2200, "Uttar Pradesh": 900,
    "Uttarakhand": 1800, "West Bengal": 1750,
}

CROP_EMOJIS = {
    "Rice":"🌾","Wheat":"🌾","Maize":"🌽","Potato":"🥔","Onion":"🧅",
    "Sugarcane":"🎋","Cotton(lint)":"🌿","Groundnut":"🥜","Soyabean":"🫘",
    "Banana":"🍌","Coconut":"🥥","Jowar":"🌾","Bajra":"🌾","Ragi":"🌾",
    "Garlic":"🧄","Ginger":"🫚","Turmeric":"🟡","Arhar/Tur":"🫘",
    "Gram":"🫘","Moong(Green Gram)":"🫘","Urad":"🫘","Barley":"🌾",
    "Sunflower":"🌻","Rapeseed &Mustard":"🌻",
}

YIELD_TIPS = {
    "Kharif": [
        ("☔ Monsoon Prep", "Ensure proper drainage in fields before sowing. Waterlogging reduces yield by 30%."),
        ("🌱 Seed Treatment", "Treat seeds with fungicide before Kharif sowing to prevent early blight."),
        ("🐛 Pest Watch", "Check fields twice a week during August–September for stem borer and leaf folder."),
    ],
    "Rabi": [
        ("❄️ Cold Protection", "Cover nurseries at night during December–January to prevent frost damage."),
        ("💧 Irrigation Timing", "Irrigate at Crown Root Initiation stage for best Rabi wheat yields."),
        ("🌿 Weed Control", "First weeding within 20–25 days of sowing is critical for Rabi crops."),
    ],
    "Whole Year": [
        ("🔄 Crop Rotation", "Rotate between legumes and cereals each season to naturally fix soil nitrogen."),
        ("🧪 Soil Testing", "Test soil every 2 years. Balanced NPK increases yield by up to 25%."),
        ("📅 Record Keeping", "Maintain a diary of sowing dates, inputs used, and yield — it helps plan next year."),
    ],
}
DEFAULT_TIPS = [
    ("🌱 Quality Seeds", "Use certified seeds from government-approved sources for consistent yield."),
    ("💊 Balanced Fertilizer", "Follow soil test results for fertilizer doses — over-application wastes money."),
    ("📞 Expert Help", "Call Kisan Call Center 1800-180-1551 (Free, 24x7) for local crop advice."),
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def yield_rating(kg_per_ha):
    if kg_per_ha >= 4000:  return "Excellent",    "#16a34a", 95
    if kg_per_ha >= 2500:  return "Good",          "#65a30d", 72
    if kg_per_ha >= 1500:  return "Average",       "#ca8a04", 52
    return                        "Below Average", "#dc2626", 28


def render_hero():
    st.markdown("""
    <div class="yield-hero">
        <div style="font-size:2.5rem;margin-bottom:8px;">📊</div>
        <div class="yield-hero-title">Crop Yield Prediction</div>
        <div class="yield-hero-sub">Enter your field details to get an AI-powered yield forecast</div>
        <div style="margin-top:14px;">
            <span class="badge">🌾 50+ Crops</span>
            <span class="badge">🗺️ All Indian States</span>
            <span class="badge">📅 All Seasons</span>
            <span class="badge">🤖 ML Powered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:10px 0 20px 0;">
            <div style="font-size:2.5rem;">📊</div>
            <div style="font-family:'Poppins',sans-serif;font-weight:800;color:#78350f;font-size:1.2rem;">Yield Predictor</div>
            <div style="color:#6b7280;font-size:0.8rem;">AgriDoc Advisory System</div>
        </div>
        <div class="sidebar-card">
            <div class="sidebar-title">📋 How to Use</div>
            <ol style="padding-left:16px;color:#4b5563;font-size:0.88rem;margin:0;line-height:2.2;">
                <li>Select your state</li>
                <li>Choose crop &amp; season</li>
                <li>Enter field area (hectares)</li>
                <li>Enter annual rainfall (mm)</li>
                <li>Set irrigation coverage (%)</li>
                <li>Click Predict My Yield</li>
            </ol>
        </div>
        <div class="sidebar-card">
            <div class="sidebar-title">📏 Unit Guide</div>
            <div style="color:#4b5563;font-size:0.85rem;line-height:2;">
                <b>Area:</b> 1 Hectare = 2.47 Acres<br>
                <b>Rainfall:</b> Enter in mm/year<br>
                <b>Irrigation:</b> % of field covered<br>
                <b>Yield:</b> Result in Kg/Hectare<br>
                <b>Avg rain:</b> India ~1083 mm/yr
            </div>
        </div>
        <div class="sidebar-card" style="background:#fffbeb;">
            <div class="sidebar-title">🌧️ Avg Rainfall by State</div>
            <div style="color:#4b5563;font-size:0.82rem;line-height:2;">
                Kerala: ~3000 mm<br>
                Punjab: ~650 mm<br>
                Rajasthan: ~330 mm<br>
                West Bengal: ~1750 mm<br>
                Maharashtra: ~1150 mm<br>
                UP: ~900 mm
            </div>
        </div>
        <div class="sidebar-card" style="background:#eff6ff;">
            <div class="sidebar-title">💧 Irrigation Guide</div>
            <div style="color:#4b5563;font-size:0.82rem;line-height:2;">
                Punjab: ~98% irrigated<br>
                Haryana: ~85% irrigated<br>
                UP: ~75% irrigated<br>
                Kerala: ~15% irrigated<br>
                Rajasthan: ~35% irrigated
            </div>
        </div>
        <div style="background:linear-gradient(135deg,#78350f,#b45309);border-radius:12px;padding:16px;text-align:center;color:white;">
            <div style="font-size:1.4rem;margin-bottom:4px;">🆘</div>
            <div style="font-weight:700;font-size:0.9rem;">Kisan Call Center</div>
            <div style="font-size:1.3rem;font-weight:800;font-family:'Poppins',sans-serif;margin:4px 0;">
                1800-180-1551
            </div>
            <div style="font-size:0.72rem;opacity:0.85;">Free · 24x7 · All Languages</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FIX: state added as parameter here ↓
# ─────────────────────────────────────────────
def render_result(result, crop, season, area, rainfall, irrigation_pct, state):
    total_kg    = result.get("total_production", 0)
    per_ha      = result.get("adjusted_yield", 0)
    base_per_ha = result.get("yield_per_ha", 0)
    rf_factor   = result.get("rainfall_factor", 1.0)
    irr_factor  = result.get("irrigation_factor", 1.0)
    combined    = result.get("combined_factor", 1.0)
    total_ton   = total_kg / 1000
    rating, r_color, r_pct = yield_rating(per_ha)
    crop_icon   = CROP_EMOJIS.get(crop, "🌾")

    src = result.get("prediction_source", "ml")
    src_badge = {
        "ml":        "🤖 ML Predicted",
        "benchmark": "📊 Benchmark Based",
        "blended":   "🔀 ML + Benchmark Blend",
    }.get(src, "⚠️ ML Capped")

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:0.9rem;opacity:0.7;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
            Predicted Yield for {crop_icon} {crop}
        </div>
        <div class="result-number">{total_kg:,.0f}</div>
        <div class="result-unit">Kilograms total</div>
        <div class="result-label">
            {area:.1f} ha · {season} · {rainfall:.0f}mm rain · {irrigation_pct:.0f}% irrigated
        </div>
        <div style="margin-top:10px;">
            <span style="background:rgba(255,255,255,0.2);border-radius:20px;
                  padding:4px 14px;font-size:0.75rem;font-weight:700;">
                {src_badge}
            </span>
        </div>
        <div class="insight-row">
            <div class="insight-chip">
                <div class="insight-val">{per_ha:,.0f}</div>
                <div class="insight-lbl">Kg / Hectare</div>
            </div>
            <div class="insight-chip">
                <div class="insight-val">{total_ton:.1f}T</div>
                <div class="insight-lbl">Total Tonnes</div>
            </div>
            <div class="insight-chip">
                <div class="insight-val">{rating}</div>
                <div class="insight-lbl">Yield Rating</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Calculation breakdown ──
    st.markdown(f"""
    <div style="background:white;border-radius:16px;padding:20px 24px;
         box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-top:16px;">
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#374151;
             margin-bottom:14px;font-size:0.95rem;">⚙️ How Your Yield Was Calculated</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
            <div style="flex:1;min-width:120px;background:#fef3c7;border-radius:10px;
                 padding:12px;text-align:center;">
                <div style="font-size:0.72rem;color:#78350f;font-weight:700;
                     text-transform:uppercase;margin-bottom:4px;">Base ML Yield</div>
                <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;
                     font-weight:800;color:#78350f;">{base_per_ha:,.0f}</div>
                <div style="font-size:0.72rem;color:#92400e;">Kg/Ha</div>
            </div>
            <div style="flex:1;min-width:120px;background:#eff6ff;border-radius:10px;
                 padding:12px;text-align:center;">
                <div style="font-size:0.72rem;color:#1e40af;font-weight:700;
                     text-transform:uppercase;margin-bottom:4px;">🌧️ Rainfall Factor</div>
                <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;
                     font-weight:800;color:#1e40af;">{rf_factor:.3f}×</div>
                <div style="font-size:0.72rem;color:#1e40af;">{rainfall:.0f} mm</div>
            </div>
            <div style="flex:1;min-width:120px;background:#f0fdf4;border-radius:10px;
                 padding:12px;text-align:center;">
                <div style="font-size:0.72rem;color:#14532d;font-weight:700;
                     text-transform:uppercase;margin-bottom:4px;">💧 Irrigation Factor</div>
                <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;
                     font-weight:800;color:#14532d;">{irr_factor:.3f}×</div>
                <div style="font-size:0.72rem;color:#14532d;">{irrigation_pct:.0f}% covered</div>
            </div>
            <div style="flex:1;min-width:120px;background:linear-gradient(135deg,#78350f,#b45309);
                 border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.8);font-weight:700;
                     text-transform:uppercase;margin-bottom:4px;">Final Yield</div>
                <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;
                     font-weight:800;color:#fde68a;">{per_ha:,.0f}</div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.7);">Kg/Ha</div>
            </div>
        </div>
        <div style="background:#fef9c3;border-radius:8px;padding:10px 14px;
             font-size:0.82rem;color:#713f12;font-weight:600;">
            📐 Formula: {base_per_ha:,.0f} × {rf_factor:.3f} (rain) × {irr_factor:.3f} (irrigation)
            = <b>{per_ha:,.0f} Kg/Ha</b> · Combined factor: <b>{combined:.3f}×</b>
        </div>
        <div style="background:#f0fdf4;border-radius:8px;padding:10px 14px;
             font-size:0.82rem;color:#14532d;font-weight:600;margin-top:8px;">
            📊 {state} benchmark for {crop}:
            <b>{result.get('expected_kg_ha', 0):,.0f} Kg/Ha</b>
            &nbsp;·&nbsp; State multiplier: <b>{result.get('state_multiplier', 1.0):.2f}×</b>
            &nbsp;·&nbsp; Source: <b>{src.upper()}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Rating bar ──
    st.markdown(f"""
    <div style="background:white;border-radius:16px;padding:20px 24px;
         box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-top:16px;">
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#374151;
             margin-bottom:10px;font-size:0.95rem;">📈 Yield Performance</div>
        <div style="display:flex;justify-content:space-between;
             font-size:0.78rem;color:#9ca3af;font-weight:700;margin-bottom:4px;">
            <span>Below Average</span><span>Average</span><span>Good</span><span>Excellent</span>
        </div>
        <div class="rating-bar-bg">
            <div class="rating-bar-fill" style="width:{r_pct}%;background:{r_color};"></div>
        </div>
        <div style="text-align:right;font-size:0.82rem;color:{r_color};font-weight:700;margin-top:4px;">
            {r_pct}% — {rating}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Recommendations ──
    try:
        recs = get_recommendations(result)

        all_advice = recs.get("rain_advice", []) + recs.get("irr_advice", [])
        if all_advice:
            st.markdown("""
            <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#1e40af;
                 margin:24px 0 10px 0;font-size:1rem;padding-bottom:8px;
                 border-bottom:2px solid #bfdbfe;">
                💧 Water Management Advice
            </div>
            """, unsafe_allow_html=True)
            for adv in all_advice:
                st.markdown(f'<div class="advice-card">{adv}</div>', unsafe_allow_html=True)

        tips = YIELD_TIPS.get(season, DEFAULT_TIPS)
        st.markdown("""
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#78350f;
             margin:24px 0 12px 0;font-size:1rem;padding-bottom:8px;
             border-bottom:2px solid #fde68a;">
            💡 Tips to Maximise Your Yield
        </div>
        """, unsafe_allow_html=True)
        for title, body in tips:
            st.markdown(f"""
            <div class="tip-card">
                <div class="tip-title">{title}</div>
                <div class="tip-body">{body}</div>
            </div>
            """, unsafe_allow_html=True)

        if recs.get("season_tip"):
            st.markdown(f"""
            <div style="background:#fef3c7;border-radius:10px;padding:12px 16px;
                 margin-top:8px;font-size:0.85rem;color:#78350f;font-weight:600;
                 border-left:4px solid #f59e0b;">
                📅 {recs['season_tip']}
            </div>
            """, unsafe_allow_html=True)

    except Exception:
        pass


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    load_css()
    render_sidebar()
    render_hero()

    if st.button("← Back to Home", key="back_home_yield"):
        st.switch_page("home.py")

    st.markdown("<br>", unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1.1], gap="large")

    with col_form:

        st.markdown("""
        <div class="section-card">
            <div class="section-header">🌾 Crop &amp; Location Details</div>
        </div>
        """, unsafe_allow_html=True)

        state = st.selectbox(
            "🗺️ Your State", STATES,
            index=STATES.index("Uttar Pradesh") if "Uttar Pradesh" in STATES else 0,
            help="Select the Indian state where your field is located",
            key="state_select"
        )
        crop = st.selectbox(
            "🌱 Crop Name", CROPS,
            index=CROPS.index("Rice") if "Rice" in CROPS else 0,
            help="Select the crop you are growing or planning to grow",
            key="crop_select"
        )
        season = st.selectbox(
            "📅 Season", SEASONS,
            help="Kharif = June–Nov | Rabi = Nov–Apr | Whole Year = perennial crops",
            key="season_select"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <div class="section-header">📏 Field &amp; Weather Details</div>
        </div>
        """, unsafe_allow_html=True)

        area = st.number_input(
            "📐 Field Area (in Hectares)",
            min_value=0.1, max_value=10000.0,
            value=1.0, step=0.5, format="%.1f",
            help="1 Hectare = 2.47 Acres.",
            key="area_input"
        )
        st.markdown("""
        <div style="background:#fef3c7;border-radius:10px;padding:10px 14px;
             margin:-8px 0 16px 0;font-size:0.82rem;color:#78350f;font-weight:600;">
            💡 <b>{:.2f} Acres</b> &nbsp;|&nbsp; <b>{:.0f} Bigha</b> (approx, varies by state)
        </div>
        """.format(area * 2.471, area * 4.0), unsafe_allow_html=True)

        default_rain = STATE_RAINFALL_DEFAULTS.get(state, 1083)
        rainfall = st.number_input(
            "🌧️ Annual Rainfall (mm)",
            min_value=10.0, max_value=5000.0,
            value=float(default_rain), step=50.0, format="%.0f",
            help="Auto-filled from state average — adjust if you know your local value.",
            key="rainfall_input"
        )

        if rainfall < 500:
            rain_note, rain_color, rain_text = "⚠️ Low rainfall region — consider drip irrigation", "#fef2f2", "#991b1b"
        elif rainfall < 1000:
            rain_note, rain_color, rain_text = "✅ Moderate rainfall — suitable for most Rabi crops", "#fefce8", "#78350f"
        elif rainfall < 2000:
            rain_note, rain_color, rain_text = "✅ Good rainfall — ideal for Kharif crops like Rice & Maize", "#f0fdf4", "#14532d"
        else:
            rain_note, rain_color, rain_text = "💧 Very high rainfall — ensure proper field drainage", "#eff6ff", "#1e3a8a"

        st.markdown(f"""
        <div style="background:{rain_color};border-radius:10px;padding:10px 14px;
             margin:-8px 0 20px 0;font-size:0.82rem;color:{rain_text};font-weight:600;">
            {rain_note}
        </div>
        """, unsafe_allow_html=True)

        irrigation_pct = st.slider(
            "💧 Irrigation Coverage (%)",
            min_value=0, max_value=100, value=50, step=5,
            help="What % of your field has access to irrigation?",
            key="irrigation_slider"
        )

        if irrigation_pct == 0:
            irr_note, irr_color, irr_text = "🌧️ Fully rain-fed — yield depends entirely on monsoon", "#fef2f2", "#991b1b"
        elif irrigation_pct < 25:
            irr_note, irr_color, irr_text = "⚠️ Very low irrigation — high monsoon dependency", "#fef2f2", "#991b1b"
        elif irrigation_pct < 50:
            irr_note, irr_color, irr_text = "🟡 Partial irrigation — supplemental water available", "#fefce8", "#78350f"
        elif irrigation_pct < 75:
            irr_note, irr_color, irr_text = "✅ Good irrigation — suitable for both Kharif and Rabi", "#f0fdf4", "#14532d"
        else:
            irr_note, irr_color, irr_text = "💧 Well irrigated — optimal water management", "#eff6ff", "#1e3a8a"

        st.markdown(f"""
        <div style="background:{irr_color};border-radius:10px;padding:10px 14px;
             margin:-8px 0 20px 0;font-size:0.82rem;color:{irr_text};font-weight:600;">
            {irr_note}
        </div>
        """, unsafe_allow_html=True)

        predict_clicked = st.button(
            "📊  Predict My Yield",
            type="primary", use_container_width=True,
            key="predict_btn"
        )

    with col_result:
        if predict_clicked:
            with st.spinner("🤖 Calculating yield prediction..."):
                try:
                    result = predict_yield(
                        crop=crop, state=state, season=season,
                        area=area, annual_rainfall=rainfall,
                        irrigation_pct=irrigation_pct,
                    )
                    st.session_state["yield_result"] = result
                    st.session_state["yield_meta"] = {
                        "crop": crop, "season": season, "area": area,
                        "rainfall": rainfall, "irrigation_pct": irrigation_pct,
                        "state": state,                  # ← state saved here
                    }
                except Exception as e:
                    st.error(f"⚠️ Prediction error: {e}")
                    st.info("Make sure your yield model is trained. Run `python yield_model.py` first.")

        if "yield_result" in st.session_state and "yield_meta" in st.session_state:
            meta = st.session_state["yield_meta"]
            render_result(
                st.session_state["yield_result"],
                meta["crop"],
                meta["season"],
                meta["area"],
                meta["rainfall"],
                meta["irrigation_pct"],
                meta["state"],           # ← state passed here ✅
            )
        else:
            crop_icon = CROP_EMOJIS.get(crop, "🌾")
            st.markdown(f"""
            <div class="await-box">
                <div style="font-size:5rem;margin-bottom:16px;opacity:0.35;">{crop_icon}</div>
                <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:700;
                     color:#374151;margin-bottom:10px;">Your yield prediction will appear here</div>
                <div style="color:#9ca3af;font-size:0.9rem;max-width:280px;
                     margin:0 auto;line-height:1.7;">
                    Fill in your field details on the left and click
                    <strong>Predict My Yield</strong> to see results
                </div>
                <div style="margin-top:24px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
                    <div style="background:#fef3c7;border-radius:10px;padding:10px 16px;
                         font-size:0.82rem;color:#78350f;font-weight:700;">📍 {state}</div>
                    <div style="background:#fef3c7;border-radius:10px;padding:10px 16px;
                         font-size:0.82rem;color:#78350f;font-weight:700;">🌱 {crop}</div>
                    <div style="background:#fef3c7;border-radius:10px;padding:10px 16px;
                         font-size:0.82rem;color:#78350f;font-weight:700;">📅 {season}</div>
                    <div style="background:#eff6ff;border-radius:10px;padding:10px 16px;
                         font-size:0.82rem;color:#1e40af;font-weight:700;">🌧️ {rainfall:.0f}mm</div>
                    <div style="background:#f0fdf4;border-radius:10px;padding:10px 16px;
                         font-size:0.82rem;color:#14532d;font-weight:700;">💧 {irrigation_pct}% irrigated</div>
                </div>
            </div>

            <div style="background:white;border-radius:16px;padding:20px 24px;
                 box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-top:20px;">
                <div style="font-family:'Poppins',sans-serif;font-weight:700;
                     color:#78350f;margin-bottom:14px;">📊 National Average Yields (Reference)</div>
                <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
                    <tr style="background:#fef3c7;">
                        <th style="padding:8px 12px;text-align:left;color:#78350f;">Crop</th>
                        <th style="padding:8px 12px;text-align:right;color:#78350f;">Avg Yield (Kg/Ha)</th>
                        <th style="padding:8px 12px;text-align:right;color:#78350f;">Season</th>
                    </tr>
                    <tr><td style="padding:8px 12px;">🌾 Rice</td><td style="padding:8px 12px;text-align:right;">2,200</td><td style="padding:8px 12px;text-align:right;">Kharif</td></tr>
                    <tr style="background:#fffbeb;"><td style="padding:8px 12px;">🌾 Wheat</td><td style="padding:8px 12px;text-align:right;">3,200</td><td style="padding:8px 12px;text-align:right;">Rabi</td></tr>
                    <tr><td style="padding:8px 12px;">🌽 Maize</td><td style="padding:8px 12px;text-align:right;">2,800</td><td style="padding:8px 12px;text-align:right;">Kharif</td></tr>
                    <tr style="background:#fffbeb;"><td style="padding:8px 12px;">🥔 Potato</td><td style="padding:8px 12px;text-align:right;">22,000</td><td style="padding:8px 12px;text-align:right;">Rabi</td></tr>
                    <tr><td style="padding:8px 12px;">🌻 Sunflower</td><td style="padding:8px 12px;text-align:right;">900</td><td style="padding:8px 12px;text-align:right;">Rabi</td></tr>
                    <tr style="background:#fffbeb;"><td style="padding:8px 12px;">🥜 Groundnut</td><td style="padding:8px 12px;text-align:right;">1,400</td><td style="padding:8px 12px;text-align:right;">Kharif</td></tr>
                    <tr><td style="padding:8px 12px;">🧅 Onion</td><td style="padding:8px 12px;text-align:right;">16,000</td><td style="padding:8px 12px;text-align:right;">Rabi</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
