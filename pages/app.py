# app.py — Intelligent Agri Advisory System
# Full featured: Disease detection, pesticides, weather, tips, report download

import streamlit as st
from PIL import Image
import time
import json
import os

from predict import predict_disease, load_model, format_class_name
from disease_info import get_disease_info, get_severity_color, is_healthy

st.set_page_config(
    page_title="Plant Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    * { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }

    /* ── App background: deep forest dark ── */
    .stApp {
        background: #0a1a0f;
        background-image:
            radial-gradient(ellipse at 20% 10%, rgba(34,197,94,0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(21,128,61,0.10) 0%, transparent 50%);
        min-height: 100vh;
    }

    /* ── hide streamlit chrome ── */
    #MainMenu, footer, .stDeployButton, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; max-width: 1400px !important; }

    /* ── HERO ── */
    .hero-header {
        background: linear-gradient(135deg, #052e16 0%, #14532d 50%, #166534 100%);
        border: 1px solid rgba(74,222,128,0.2);
        border-radius: 24px;
        padding: 44px 36px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 0 60px rgba(22,163,74,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 3rem; font-weight: 800;
        color: #f0fdf4;
        letter-spacing: -1px;
        margin: 0 0 8px 0;
        text-shadow: 0 0 40px rgba(74,222,128,0.3);
    }
    .hero-title span { color: #4ade80; }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(220,252,231,0.75);
        margin: 0 0 20px 0;
        font-weight: 400;
    }
    .badge {
        background: rgba(74,222,128,0.12);
        border: 1px solid rgba(74,222,128,0.25);
        color: #86efac;
        padding: 5px 14px; border-radius: 30px;
        font-size: 0.8rem; font-weight: 600;
        display: inline-block; margin: 3px;
        letter-spacing: 0.2px;
    }

    /* ── STATS ROW ── */
    .stats-row { display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
    .stat-box {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(74,222,128,0.15);
        border-radius: 16px;
        padding: 18px 12px;
        text-align: center;
        min-width: 80px;
        transition: border-color 0.2s, background 0.2s;
    }
    .stat-box:hover {
        background: rgba(74,222,128,0.07);
        border-color: rgba(74,222,128,0.35);
    }
    .stat-number {
        font-family: 'Syne', sans-serif;
        font-size: 1.7rem; font-weight: 800;
        color: #4ade80; line-height: 1;
    }
    .stat-label {
        font-size: 0.68rem; color: rgba(220,252,231,0.55);
        font-weight: 600; text-transform: uppercase;
        letter-spacing: 1.2px; margin-top: 5px;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(74,222,128,0.12) !important;
        border-radius: 14px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: rgba(220,252,231,0.6) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        transition: all 0.2s !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #86efac !important;
        background: rgba(74,222,128,0.08) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #16a34a, #15803d) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(22,163,74,0.4) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

    /* ── TOGGLE ── */
    .stToggle label { color: #86efac !important; font-weight: 600 !important; }

    /* ── UPLOAD ZONE ── */
    .upload-zone {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(74,222,128,0.3);
        border-radius: 20px; padding: 28px;
        text-align: center;
        transition: all 0.3s;
    }
    .upload-zone:hover {
        border-color: rgba(74,222,128,0.6);
        background: rgba(74,222,128,0.04);
    }
    .upload-zone-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.2rem; font-weight: 700;
        color: #dcfce7; margin: 10px 0 6px 0;
    }
    .upload-zone-sub { color: rgba(220,252,231,0.5); font-size: 0.88rem; }
    div[data-testid="stFileUploadDropzone"] { background: transparent !important; border: none !important; }
    div[data-testid="stFileUploadDropzone"] * { color: #86efac !important; }

    /* ── RESULT CARD ── */
    .result-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(74,222,128,0.15);
        border-radius: 20px; padding: 28px;
        margin-bottom: 16px;
        animation: slideIn 0.4s ease-out both;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .disease-name {
        font-family: 'Syne', sans-serif;
        font-size: 1.55rem; font-weight: 700; color: #f0fdf4;
    }
    .crop-badge {
        display: inline-block;
        background: rgba(74,222,128,0.15);
        border: 1px solid rgba(74,222,128,0.25);
        color: #86efac;
        padding: 3px 12px; border-radius: 20px;
        font-size: 0.82rem; font-weight: 600;
    }

    /* ── SEVERITY BADGES ── */
    .severity-badge {
        display: inline-block; padding: 4px 14px;
        border-radius: 20px; font-weight: 700; font-size: 0.82rem;
        border: 1px solid transparent;
    }
    .severity-none     { background: rgba(74,222,128,0.15);  color: #86efac;  border-color: rgba(74,222,128,0.25); }
    .severity-low      { background: rgba(250,204,21,0.15);  color: #fde047;  border-color: rgba(250,204,21,0.25); }
    .severity-medium   { background: rgba(251,146,60,0.15);  color: #fb923c;  border-color: rgba(251,146,60,0.25); }
    .severity-high     { background: rgba(248,113,113,0.15); color: #f87171;  border-color: rgba(248,113,113,0.25); }
    .severity-very-high{ background: rgba(192,132,252,0.15); color: #c084fc;  border-color: rgba(192,132,252,0.25); }

    /* ── CONFIDENCE BAR ── */
    .confidence-bar-container {
        background: rgba(255,255,255,0.08);
        border-radius: 8px; height: 10px; overflow: hidden; margin: 8px 0;
    }
    .confidence-bar { height: 100%; border-radius: 8px; transition: width 1s ease-out; }

    /* ── SECTION HEADER ── */
    .section-header {
        font-family: 'Syne', sans-serif;
        font-size: 1rem; font-weight: 700; color: #4ade80;
        margin: 20px 0 12px 0; padding-bottom: 8px;
        border-bottom: 1px solid rgba(74,222,128,0.2);
        letter-spacing: 0.3px;
    }

    /* ── SYMPTOM ITEMS ── */
    .symptom-item {
        background: rgba(250,204,21,0.07);
        border: 1px solid rgba(250,204,21,0.15);
        border-left: 3px solid #fde047;
        border-radius: 8px; padding: 8px 12px;
        margin-bottom: 6px; font-size: 0.88rem; color: #fef9c3;
    }

    /* ── PESTICIDE CARD ── */
    .pesticide-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(74,222,128,0.15);
        border-left: 3px solid #16a34a;
        border-radius: 14px; padding: 18px; margin-bottom: 12px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .pesticide-card:hover {
        transform: translateX(4px);
        border-color: rgba(74,222,128,0.35);
        background: rgba(74,222,128,0.05);
    }
    .pesticide-number {
        background: linear-gradient(135deg, #16a34a, #15803d);
        color: white; border-radius: 50%;
        width: 28px; height: 28px;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.85rem;
    }
    .pesticide-name { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: #f0fdf4; }
    .pesticide-type { font-size: 0.75rem; color: rgba(220,252,231,0.5); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .detail-chip {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(74,222,128,0.2);
        border-radius: 8px; padding: 3px 10px;
        font-size: 0.78rem; color: #86efac;
        display: inline-block; margin: 3px; font-weight: 500;
    }

    /* ── PREVENTION BOX ── */
    .prevention-box {
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.2);
        border-left: 3px solid #60a5fa;
        border-radius: 12px; padding: 16px; margin-top: 16px;
    }
    .prevention-title { font-weight: 700; color: #93c5fd; margin-bottom: 6px; font-size: 0.92rem; }
    .prevention-text { color: rgba(219,234,254,0.85); font-size: 0.88rem; line-height: 1.7; }

    /* ── HEALTHY BANNER ── */
    .healthy-banner {
        background: linear-gradient(135deg, #052e16 0%, #14532d 50%, #15803d 100%);
        border: 1px solid rgba(74,222,128,0.3);
        border-radius: 24px; padding: 48px 36px;
        text-align: center;
        box-shadow: 0 0 60px rgba(22,163,74,0.2);
        animation: slideIn 0.4s ease-out;
    }
    .healthy-title {
        font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800;
        color: #f0fdf4; margin-bottom: 10px;
    }
    .healthy-sub { opacity: 0.85; font-size: 1rem; color: #dcfce7; }

    /* ── PREDICTION ROW ── */
    .prediction-row {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 8px; padding: 10px 14px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(74,222,128,0.08);
        border-radius: 10px; transition: background 0.2s;
    }
    .prediction-row:hover { background: rgba(74,222,128,0.05); }
    .prediction-rank { font-weight: 700; color: rgba(220,252,231,0.4); width: 24px; }
    .prediction-name { flex: 1; font-size: 0.88rem; color: #dcfce7; }
    .prediction-pct  { font-weight: 700; color: #4ade80; font-size: 0.88rem; min-width: 50px; text-align: right; }

    /* ── TTA BADGE ── */
    .tta-badge {
        background: rgba(96,165,250,0.15); border: 1px solid rgba(96,165,250,0.25);
        color: #93c5fd; padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; display: inline-block; margin-left: 8px;
    }

    /* ── DEMO WARNING ── */
    .demo-warning {
        background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3);
        border-radius: 12px; padding: 12px 16px; margin-bottom: 16px;
        font-size: 0.85rem; color: #fde68a;
    }

    /* ── TIP CARD ── */
    .tip-card {
        background: rgba(250,204,21,0.06); border: 1px solid rgba(250,204,21,0.15);
        border-left: 3px solid #fde047; border-radius: 12px;
        padding: 14px; margin-bottom: 10px;
    }
    .tip-title { font-weight: 700; color: #fde047; margin-bottom: 4px; font-size: 0.9rem; }
    .tip-text  { color: rgba(254,249,195,0.8); font-size: 0.85rem; line-height: 1.6; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: #050f08 !important;
        border-right: 1px solid rgba(74,222,128,0.1) !important;
    }
    section[data-testid="stSidebar"] * { color: #dcfce7 !important; }
    .sidebar-card {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(74,222,128,0.12);
        border-radius: 14px; padding: 16px; margin-bottom: 12px;
    }
    .sidebar-card-title {
        font-family: 'Syne', sans-serif; font-weight: 700;
        color: #4ade80 !important; margin-bottom: 10px; font-size: 0.92rem;
    }
    .sidebar-text { color: rgba(220,252,231,0.7) !important; font-size: 0.83rem; line-height: 2; }

    /* ── STREAMLIT BUTTON ── */
    div.stButton > button {
        background: linear-gradient(135deg, #16a34a, #15803d) !important;
        color: #ffffff !important; border: none !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important; font-size: 0.95rem !important;
        padding: 14px 0 !important;
        box-shadow: 0 4px 20px rgba(22,163,74,0.35) !important;
        transition: all 0.2s !important; letter-spacing: 0.3px !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 6px 28px rgba(22,163,74,0.55) !important;
        transform: translateY(-2px) !important;
    }

    /* ── FILE UPLOADER ── */
    [data-testid="stFileUploader"] button {
        background: rgba(74,222,128,0.12) !important;
        border: 1px solid rgba(74,222,128,0.3) !important;
        color: #86efac !important; border-radius: 10px !important;
    }

    /* ── SELECTBOX / TEXT INPUT ── */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(74,222,128,0.2) !important;
        border-radius: 10px !important; color: #dcfce7 !important;
    }
    .stSelectbox label, .stTextInput label { color: #86efac !important; font-weight: 600 !important; }

    /* ── AWAITING PLACEHOLDER ── */
    .awaiting-box {
        height: 420px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(74,222,128,0.1);
        border-radius: 20px; text-align: center; padding: 30px;
    }
    .awaiting-icon { font-size: 5rem; margin-bottom: 16px; opacity: 0.2; }
    .awaiting-title { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: #dcfce7; margin-bottom: 10px; }
    .awaiting-sub { color: rgba(220,252,231,0.4); font-size: 0.88rem; max-width: 280px; line-height: 1.7; }

    /* ── DISEASE LIBRARY CARD ── */
    .lib-card {
        background: rgba(255,255,255,0.03);
        border-radius: 14px; padding: 16px;
        border-top: 3px solid var(--border-color);
        border-left: 1px solid rgba(255,255,255,0.06);
        border-right: 1px solid rgba(255,255,255,0.06);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 14px; min-height: 140px; transition: background 0.2s;
    }
    .lib-card:hover { background: rgba(74,222,128,0.04); }
    .lib-card-title { font-family: 'Syne', sans-serif; font-weight: 700; color: #f0fdf4; font-size: 0.92rem; margin-bottom: 6px; }
    .lib-crop-tag {
        background: rgba(74,222,128,0.12); color: #86efac;
        padding: 2px 8px; border-radius: 10px; font-size: 0.72rem;
        font-weight: 600; display: inline-block; margin-bottom: 8px;
    }
    .lib-desc { font-size: 0.78rem; color: rgba(220,252,231,0.5); line-height: 1.5; }

    /* ── EMERGENCY CARD ── */
    .emergency-card {
        background: rgba(239,68,68,0.07); border: 1px solid rgba(239,68,68,0.2);
        border-left: 3px solid #f87171; border-radius: 10px;
        padding: 12px; margin-bottom: 8px;
    }
    .emergency-sign   { font-weight: 700; color: #fca5a5; font-size: 0.87rem; }
    .emergency-action { color: rgba(254,226,226,0.7); font-size: 0.81rem; margin-top: 4px; }

    /* ── TECH TAG ── */
    .tech-tag {
        display: inline-block; padding: 4px 12px;
        border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin: 4px;
    }

    /* ── KISAN CARD ── */
    .kisan-card {
        background: linear-gradient(135deg, #052e16, #14532d);
        border: 1px solid rgba(74,222,128,0.25);
        border-radius: 14px; padding: 18px; text-align: center;
    }
    .kisan-number {
        font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800;
        color: #4ade80 !important; margin: 6px 0;
    }

    /* ── IMAGE META ── */
    .img-meta {
        background: rgba(255,255,255,0.05); border-radius: 8px;
        padding: 8px 14px; margin-top: 6px; font-size: 0.8rem;
        color: rgba(220,252,231,0.5);
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a1a0f; }
    ::-webkit-scrollbar-thumb { background: rgba(74,222,128,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────
def severity_badge(severity):
    css = f"severity-{severity.lower().replace(' ','-')}"
    icon = {"None":"✅","Low":"🟡","Medium":"🟠","High":"🔴","Very High":"🟣"}.get(severity,"⚠️")
    return f'<span class="severity-badge {css}">{icon} {severity} Severity</span>'


def render_hero():
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🌿 <span>Plant Disease </span>Detector</div>
        <div class="hero-subtitle">AI-Powered Plant Disease Detection &amp; Pesticide Advisor</div>
        <div>
            <span class="badge">📸 Photo Diagnosis</span>
            <span class="badge">🦠 38 Diseases</span>
            <span class="badge">💊 Top 5 Pesticides</span>
            <span class="badge">🔬 EfficientNetB3</span>
            <span class="badge">🎯 97%+ Accuracy</span>
            <span class="badge">🔁 TTA Enhanced</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats():
    acc = "97%+"
    if os.path.exists("models/training_summary.json"):
        try:
            with open("models/training_summary.json") as f:
                s = json.load(f)
            acc = f"{s.get('val_accuracy', 97)}%"
        except:
            pass

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-number">38</div><div class="stat-label">Diseases</div></div>
        <div class="stat-box"><div class="stat-number">14</div><div class="stat-label">Crops</div></div>
        <div class="stat-box"><div class="stat-number">{acc}</div><div class="stat-label">Accuracy</div></div>
        <div class="stat-box"><div class="stat-number">5</div><div class="stat-label">Pesticides</div></div>
        <div class="stat-box"><div class="stat-number">TTA</div><div class="stat-label">Enhanced</div></div>
    </div>
    """, unsafe_allow_html=True)


def render_healthy(disease_info):
    st.markdown(f"""
    <div class="healthy-banner">
        <div style="font-size:4rem;margin-bottom:12px;">✅</div>
        <div class="healthy-title">Your Plant is Healthy!</div>
        <div class="healthy-sub">
            No disease detected in this <strong>{disease_info.get('crop','plant')}</strong> leaf.<br>
            Keep up the good farming practices! 🎉
        </div>
    </div>
    <div class="prevention-box" style="margin-top:20px;">
        <div class="prevention-title">💡 Tips to Keep Your Plant Healthy</div>
        <div class="prevention-text">{disease_info.get('prevention','Regular monitoring and balanced fertilization.')}</div>
    </div>
    """, unsafe_allow_html=True)


def render_disease_card(result, disease_info):
    conf = result["confidence"]
    tta_label = '<span class="tta-badge">🔁 TTA Enhanced</span>' if result.get("tta_used") else ""

    if result.get("demo_mode"):
        st.markdown("""
        <div class="demo-warning">
            ⚠️ <strong>Demo Mode:</strong> Train the model first using <code>python model.py</code>.
            Results shown are for interface demonstration only.
        </div>""", unsafe_allow_html=True)

    bar_color = '#4ade80' if conf > 80 else '#fbbf24' if conf > 50 else '#f87171'

    st.markdown(f"""
    <div class="result-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
            <div>
                <div class="disease-name">🦠 {disease_info['common_name']} {tta_label}</div>
                <div style="margin:10px 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
                    <span class="crop-badge">🌱 {disease_info['crop']}</span>
                    {severity_badge(disease_info['severity'])}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#4ade80;line-height:1;">
                    {conf:.1f}%
                </div>
                <div style="font-size:0.72rem;color:rgba(220,252,231,0.45);font-weight:600;letter-spacing:1px;text-transform:uppercase;">Confidence</div>
            </div>
        </div>
        <div style="margin-top:14px;">
            <div style="font-size:0.72rem;color:rgba(220,252,231,0.4);font-weight:600;margin-bottom:5px;letter-spacing:1px;text-transform:uppercase;">Confidence Score</div>
            <div class="confidence-bar-container">
                <div class="confidence-bar" style="width:{min(conf,100):.1f}%;background:{bar_color};"></div>
            </div>
        </div>
        <p style="color:rgba(220,252,231,0.75);margin-top:16px;font-size:0.92rem;line-height:1.75;">
            {disease_info['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_symptoms(disease_info):
    symptoms = disease_info.get("symptoms", [])
    if not symptoms:
        return
    st.markdown('<div class="section-header">🔍 Symptoms to Watch For</div>', unsafe_allow_html=True)
    for s in symptoms:
        st.markdown(f'<div class="symptom-item">🔸 {s}</div>', unsafe_allow_html=True)


def render_pesticides(disease_info):
    pesticides = disease_info.get("pesticides", [])
    if not pesticides:
        st.info("No specific pesticides in database. Consult your local agronomist.")
        return
    st.markdown('<div class="section-header">💊 Top 5 Recommended Pesticides</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:rgba(220,252,231,0.45);font-size:0.84rem;margin-bottom:14px;">'
        '⚠️ Always wear protective equipment. Consult local agri expert before applying.</p>',
        unsafe_allow_html=True
    )
    for i, p in enumerate(pesticides, 1):
        st.markdown(f"""
        <div class="pesticide-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <span class="pesticide-number">{i}</span>
                <div>
                    <div class="pesticide-name">{p['name']}</div>
                    <div class="pesticide-type">{p['type']}</div>
                </div>
            </div>
            <div>
                <span class="detail-chip">⚗️ {p['dosage']}</span>
                <span class="detail-chip">📅 {p['frequency']}</span>
            </div>
            <div style="margin-top:10px;font-size:0.82rem;color:rgba(220,252,231,0.55);font-style:italic;">
                💡 {p['notes']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_prevention(disease_info):
    prev = disease_info.get("prevention", "")
    if not prev:
        return
    st.markdown(f"""
    <div class="prevention-box">
        <div class="prevention-title">🛡️ Prevention &amp; Best Practices</div>
        <div class="prevention-text">{prev}</div>
    </div>
    """, unsafe_allow_html=True)


def render_top5(top_predictions):
    st.markdown('<div class="section-header">📊 Model Confidence — Top 5 Predictions</div>',
                unsafe_allow_html=True)
    colors = ["#4ade80", "#22c55e", "#16a34a", "#15803d", "#166534"]
    for i, (name, conf) in enumerate(top_predictions, 1):
        readable = format_class_name(name)
        highlight = "background:rgba(74,222,128,0.07);border-color:rgba(74,222,128,0.25);" if i == 1 else ""
        st.markdown(f"""
        <div class="prediction-row" style="{highlight}">
            <span class="prediction-rank">#{i}</span>
            <span class="prediction-name">{readable}</span>
            <div style="width:100px;">
                <div style="height:6px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;">
                    <div style="width:{min(conf,100):.1f}%;height:100%;background:{colors[i-1]};border-radius:4px;"></div>
                </div>
            </div>
            <span class="prediction-pct">{conf:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)


def render_farming_tips():
    tips = [
        ("🌱 Crop Rotation", "Rotate crops every season to break disease cycles and improve soil health."),
        ("💧 Smart Irrigation", "Use drip irrigation — wet leaves attract fungal diseases. Water at base of plant."),
        ("🔍 Early Scouting", "Check your field twice a week. Early detection saves 60-80% of crop loss."),
        ("🧤 Tool Hygiene", "Disinfect pruning tools with 10% bleach solution before moving between plants."),
        ("🌞 Proper Spacing", "Adequate spacing improves air circulation and reduces humidity-related diseases."),
        ("📦 Certified Seeds", "Always use certified disease-free seeds and seedlings from trusted sources."),
    ]
    st.markdown('<div class="section-header">🌾 Smart Farming Tips</div>', unsafe_allow_html=True)
    for title, tip in tips:
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-title">{title}</div>
            <div class="tip-text">{tip}</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0 24px 0;">
            <div style="font-size:2.8rem;">🌿</div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;color:#4ade80 !important;font-size:1.4rem;">Plant Disease Detector</div>
            <div style="color:rgba(220,252,231,0.45) !important;font-size:0.78rem;margin-top:2px;">Intelligent Agri Advisory System</div>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists("models/training_summary.json"):
            try:
                with open("models/training_summary.json") as f:
                    s = json.load(f)
                st.markdown(f"""
                <div class="sidebar-card" style="border-color:rgba(74,222,128,0.2);">
                    <div class="sidebar-card-title">🎯 Model Performance</div>
                    <div class="sidebar-text">
                        🧠 {s.get('model','EfficientNetB3')}<br>
                        ✅ Val Accuracy: <strong style="color:#4ade80 !important">{s.get('val_accuracy','—')}%</strong><br>
                        🔁 TTA Accuracy: <strong style="color:#4ade80 !important">{s.get('tta_accuracy','—')}%</strong><br>
                        📦 Classes: <strong style="color:#4ade80 !important">{s.get('num_classes',38)}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except:
                pass

        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-card-title">📋 How to Use</div>
            <ol style="padding-left:16px;font-size:0.85rem;margin:0;line-height:2.2;color:rgba(220,252,231,0.7) !important;">
                <li>Upload a clear leaf photo</li>
                <li>Wait for AI analysis</li>
                <li>View disease diagnosis</li>
                <li>Check pesticide guide</li>
                <li>Follow prevention tips</li>
                <li>Download full report</li>
            </ol>
        </div>
        <div class="sidebar-card">
            <div class="sidebar-card-title">🌾 Supported Crops</div>
            <div class="sidebar-text">
                🍎 Apple &nbsp; 🍅 Tomato &nbsp; 🥔 Potato<br>
                🌽 Corn &nbsp; 🍇 Grape &nbsp; 🍑 Peach<br>
                🍓 Strawberry &nbsp; 🫑 Pepper<br>
                🌿 Soybean &nbsp; 🫐 Blueberry<br>
                🍊 Orange &nbsp; 🍒 Cherry<br>
                🎃 Squash &nbsp; 🍇 Raspberry
            </div>
        </div>
        <div class="sidebar-card">
            <div class="sidebar-card-title">📸 Photo Tips</div>
            <div class="sidebar-text">
                ✅ Clear, well-lit photo<br>
                ✅ Single leaf in frame<br>
                ✅ Show affected area clearly<br>
                ✅ Natural daylight preferred<br>
                ❌ No blurry / dark photos<br>
                ❌ Avoid strong shadows
            </div>
        </div>
        <div class="sidebar-card" style="background:rgba(239,68,68,0.06);border-color:rgba(239,68,68,0.2);">
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#fca5a5 !important;margin-bottom:6px;font-size:0.9rem;">⚠️ Disclaimer</div>
            <div style="color:rgba(254,226,226,0.6) !important;font-size:0.78rem;line-height:1.6;">
                For educational guidance only. Always consult a certified agronomist or your local
                Krishi Vigyan Kendra (KVK) before applying any pesticides.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="kisan-card">
            <div style="font-size:1.4rem;">🆘</div>
            <div style="font-weight:700;color:#dcfce7 !important;margin-top:4px;">Kisan Call Center</div>
            <div class="kisan-number">1800-180-1551</div>
            <div style="font-size:0.72rem;color:rgba(220,252,231,0.45) !important;">Free • 24x7 • All Languages</div>
        </div>
        """, unsafe_allow_html=True)


def generate_report(result, disease_info):
    pests = disease_info.get("pesticides", [])
    pest_lines = ""
    for i, p in enumerate(pests, 1):
        pest_lines += f"\n  {i}. {p['name']}\n"
        pest_lines += f"     Type      : {p['type']}\n"
        pest_lines += f"     Dosage    : {p['dosage']}\n"
        pest_lines += f"     Frequency : {p['frequency']}\n"
        pest_lines += f"     Note      : {p['notes']}\n"

    symptoms = "\n".join(f"  • {s}" for s in disease_info.get("symptoms", []))
    tta_note = "Yes (7 augmentations averaged)" if result.get("tta_used") else "No"

    top5_lines = ""
    for i, (n, c) in enumerate(result['top_predictions'], 1):
        top5_lines += f"  #{i}. {format_class_name(n)} — {c:.2f}%\n"

    return f"""
╔══════════════════════════════════════════════╗
        🌿 Plant Disease Detector Report      
╚══════════════════════════════════════════════╝

DIAGNOSIS SUMMARY
──────────────────────────────────────────────────────────────
Disease Name   : {disease_info['common_name']}
Crop           : {disease_info['crop']}
Severity       : {disease_info['severity']}
Confidence     : {result['confidence']:.2f}%
TTA Used       : {tta_note}
Raw Label      : {result['predicted_class']}
Model          : EfficientNetB3 (Transfer Learning)

DESCRIPTION
──────────────────────────────────────────────────────────────
{disease_info['description']}

SYMPTOMS TO WATCH FOR
──────────────────────────────────────────────────────────────
{symptoms if symptoms else '  No specific symptoms listed.'}

TOP 5 PESTICIDE RECOMMENDATIONS
──────────────────────────────────────────────────────────────
{pest_lines if pest_lines else '  No specific pesticides. Consult local agronomist.'}

PREVENTION & BEST PRACTICES
──────────────────────────────────────────────────────────────
  {disease_info.get('prevention', 'Consult local agronomist.')}

TOP 5 MODEL PREDICTIONS
──────────────────────────────────────────────────────────────
{top5_lines}
──────────────────────────────────────────────────────────────
⚠️  DISCLAIMER: AI-generated report for educational purposes only.
    Always consult a certified agronomist before applying pesticides.
    Project Made by: Shubhankar | Himanshu | Ritik
──────────────────────────────────────────────────────────────
Generated by Intelligent Agri Advisory System
"""


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def main():
    load_css()
    render_sidebar()
    render_hero()
    render_stats()

    @st.cache_resource(show_spinner=False)
    def get_model():
        return load_model()

    model = get_model()
    if model is None:
        st.info("ℹ️ **Demo Mode** — Model not found. Run `python model.py` to train. "
                "All UI features are fully functional for demonstration.", icon="🔬")

    tta_enabled = st.toggle("🔁 Enable TTA (Test Time Augmentation) — Higher accuracy, slightly slower",
                             value=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬  Diagnose Plant",
        "💊  Disease Library",
        "🌾  Farming Tips",
        "ℹ️  About Project"
    ])

    # ─────────────────────────────
    # TAB 1 — DIAGNOSIS
    # ─────────────────────────────
    with tab1:
        col_left, col_right = st.columns([1, 1.2], gap="large")

        with col_left:
            st.markdown("""
            <div class="upload-zone">
                <div style="font-size:3rem;">📸</div>
                <div class="upload-zone-title">Upload Leaf Photo</div>
                <div class="upload-zone-sub">Clear photo of the affected leaf for best results</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload leaf image",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed"
            )

            if uploaded_file:
                img = Image.open(uploaded_file)
                st.image(img, caption="📸 Uploaded Leaf", use_container_width=True)
                st.markdown(f"""
                <div class="img-meta">
                    📐 {img.size[0]} × {img.size[1]} px &nbsp;|&nbsp; 🎨 {img.mode}
                </div>
                """, unsafe_allow_html=True)

        with col_right:
            if uploaded_file:
                img = Image.open(uploaded_file)
                analyze = st.button("🔬  Analyze Disease Now",
                                    use_container_width=True, type="primary")

                if analyze:
                    progress = st.progress(0)
                    status = st.empty()
                    steps = [
                        (15, "🔍 Preprocessing image..."),
                        (35, "🧬 Extracting leaf features..."),
                        (55, "🦠 Identifying disease patterns..."),
                        (75, "🔁 Running TTA augmentations..." if tta_enabled else "💊 Matching disease database..."),
                        (90, "💊 Fetching pesticide recommendations..."),
                        (100, "✅ Analysis complete!")
                    ]
                    for pct, msg in steps:
                        progress.progress(pct)
                        status.markdown(
                            f'<p style="text-align:center;color:#4ade80;font-weight:600;font-size:0.95rem;">{msg}</p>',
                            unsafe_allow_html=True
                        )
                        time.sleep(0.35)
                    progress.empty()
                    status.empty()

                    result = predict_disease(img, model, use_tta=tta_enabled, tta_steps=7)
                    disease_info = get_disease_info(result["predicted_class"])
                    st.session_state["result"] = result
                    st.session_state["disease_info"] = disease_info

                if "result" in st.session_state:
                    result = st.session_state["result"]
                    disease_info = st.session_state["disease_info"]

                    if is_healthy(result["predicted_class"]):
                        render_healthy(disease_info)
                    else:
                        r1, r2, r3 = st.tabs(["🦠 Diagnosis", "💊 Pesticides", "📊 Details"])
                        with r1:
                            render_disease_card(result, disease_info)
                            render_symptoms(disease_info)
                            render_prevention(disease_info)
                        with r2:
                            render_pesticides(disease_info)
                        with r3:
                            render_top5(result["top_predictions"])
                            st.markdown("<br>", unsafe_allow_html=True)
                            report = generate_report(result, disease_info)
                            st.download_button(
                                "📥  Download Full Report (.txt)",
                                data=report,
                                file_name=f"agridoc_{result['predicted_class'][:25]}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
            else:
                st.markdown("""
                <div class="awaiting-box">
                    <div class="awaiting-icon">🌿</div>
                    <div class="awaiting-title">Awaiting Leaf Photo</div>
                    <div class="awaiting-sub">
                        Upload a photo of your plant leaf to get instant disease
                        diagnosis and treatment recommendations
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────
    # TAB 2 — DISEASE LIBRARY
    # ─────────────────────────────
    with tab2:
        from disease_info import DISEASE_DATABASE
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
             color:#f0fdf4;margin-bottom:6px;">📚 Complete Disease Library</div>
        <p style="color:rgba(220,252,231,0.45);margin-bottom:20px;font-size:0.88rem;">
            Browse all 38 plant diseases supported by IAAS.
        </p>
        """, unsafe_allow_html=True)

        crops = sorted(set(
            v["crop"] for k, v in DISEASE_DATABASE.items()
            if k != "default" and v["crop"] != "Unknown"
        ))
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            selected_crop = st.selectbox("🌾 Crop", ["All Crops"] + crops)
        with c2:
            severity_filter = st.selectbox("⚠️ Severity",
                                            ["All", "None", "Low", "Medium", "High", "Very High"])
        with c3:
            search = st.text_input("🔍 Search...", placeholder="blight, rust, mildew...")

        diseases = [
            (k, v) for k, v in DISEASE_DATABASE.items()
            if k != "default"
            and (selected_crop == "All Crops" or v["crop"] == selected_crop)
            and (severity_filter == "All" or v["severity"] == severity_filter)
            and (not search or search.lower() in v["common_name"].lower()
                 or search.lower() in v.get("description", "").lower())
        ]

        st.markdown(f'<p style="color:rgba(220,252,231,0.35);font-size:0.82rem;margin-bottom:16px;">'
                    f'Showing {len(diseases)} diseases</p>', unsafe_allow_html=True)

        if not diseases:
            st.info("No diseases match your filters.")

        for i in range(0, len(diseases), 3):
            cols = st.columns(3)
            for j, (key, info) in enumerate(diseases[i:i+3]):
                with cols[j]:
                    healthy = is_healthy(key)
                    border = {"None":"#4ade80","Low":"#fbbf24","Medium":"#f97316",
                              "High":"#ef4444","Very High":"#a855f7"}.get(info["severity"],"#6b7280")
                    icon = "✅" if healthy else "🦠"
                    st.markdown(f"""
                    <div class="lib-card" style="--border-color:{border};">
                        <div class="lib-card-title">{icon} {info['common_name']}</div>
                        <div class="lib-crop-tag">{info['crop']}</div>
                        <div class="lib-desc">{info['description'][:90]}...</div>
                        <div style="margin-top:10px;">{severity_badge(info['severity'])}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ─────────────────────────────
    # TAB 3 — FARMING TIPS
    # ─────────────────────────────
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            render_farming_tips()
        with col_b:
            st.markdown('<div class="section-header">📅 Seasonal Disease Calendar</div>',
                        unsafe_allow_html=True)
            seasons = [
                ("🌸 Spring (Feb–Apr)", "Watch for: Early Blight, Bacterial Spot, Rust. Apply preventive copper sprays before rains."),
                ("☀️ Summer (May–Jul)", "Watch for: Late Blight, TYLCV, Spider Mites. Hot dry weather — check for mites daily."),
                ("🌧️ Monsoon (Jul–Sep)", "Highest disease risk! Watch for: Late Blight, Leaf Mold, Powdery Mildew. Spray every 7 days."),
                ("🍂 Autumn (Oct–Nov)", "Watch for: Target Spot, Septoria. Remove crop debris. Prepare for next season."),
                ("❄️ Winter (Dec–Jan)", "Apply dormant sprays. Prune trees. Clean and disinfect all farming tools."),
            ]
            for season, advice in seasons:
                st.markdown(f"""
                <div class="tip-card">
                    <div class="tip-title">{season}</div>
                    <div class="tip-text">{advice}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">🚨 Emergency Signs</div>', unsafe_allow_html=True)
            emergencies = [
                ("Sudden wilting of entire plant", "Bacterial wilt / Root rot — Remove plant immediately"),
                ("White powder on all leaves", "Severe Powdery Mildew — Spray sulfur urgently"),
                ("All leaves turning yellow rapidly", "Virus infection or nutrient deficiency — Test soil"),
                ("Dark water-soaked spots spreading fast", "Late Blight — Apply Ridomil Gold within 24hrs"),
            ]
            for sign, action in emergencies:
                st.markdown(f"""
                <div class="emergency-card">
                    <div class="emergency-sign">🚨 {sign}</div>
                    <div class="emergency-action">→ {action}</div>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────
    # TAB 4 — ABOUT
    # ─────────────────────────────
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="result-card">
                <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
                     color:#4ade80;margin-bottom:14px;">🎓 About This Project</div>
                <p style="color:rgba(220,252,231,0.75);line-height:1.85;font-size:0.9rem;">
                    <strong style="color:#f0fdf4;">Intelligent Agri Advisory System</strong>
                    is a college ML project that helps farmers detect plant diseases from leaf photos
                    and get precise pesticide recommendations instantly.
                </p>
                <br>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#4ade80;margin-bottom:12px;font-size:0.9rem;">🔧 Technology Stack</div>
                <div style="display:flex;flex-wrap:wrap;gap:6px;">
                    <span class="tech-tag" style="background:rgba(59,130,246,0.15);color:#93c5fd;border:1px solid rgba(59,130,246,0.25);">TensorFlow 2.x</span>
                    <span class="tech-tag" style="background:rgba(74,222,128,0.12);color:#86efac;border:1px solid rgba(74,222,128,0.2);">EfficientNetB3</span>
                    <span class="tech-tag" style="background:rgba(250,204,21,0.12);color:#fde047;border:1px solid rgba(250,204,21,0.2);">Streamlit</span>
                    <span class="tech-tag" style="background:rgba(167,139,250,0.12);color:#c4b5fd;border:1px solid rgba(167,139,250,0.2);">Transfer Learning</span>
                    <span class="tech-tag" style="background:rgba(248,113,113,0.12);color:#fca5a5;border:1px solid rgba(248,113,113,0.2);">Mixup Augmentation</span>
                    <span class="tech-tag" style="background:rgba(56,189,248,0.12);color:#7dd3fc;border:1px solid rgba(56,189,248,0.2);">TTA Inference</span>
                    <span class="tech-tag" style="background:rgba(52,211,153,0.12);color:#6ee7b7;border:1px solid rgba(52,211,153,0.2);">Label Smoothing</span>
                    <span class="tech-tag" style="background:rgba(244,114,182,0.12);color:#f9a8d4;border:1px solid rgba(244,114,182,0.2);">PlantVillage Dataset</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="result-card">
                <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
                     color:#4ade80;margin-bottom:14px;">🧠 Model Architecture</div>
                <div style="font-size:0.86rem;line-height:2.2;">
                    <div><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Base Model</span><br><strong style="color:#f0fdf4;">EfficientNetB3 (ImageNet)</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Input Size</span><br><strong style="color:#f0fdf4;">224 × 224 × 3</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Training Strategy</span><br><strong style="color:#f0fdf4;">3-Phase (frozen → top 60 → full fine-tune)</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Augmentation</span><br><strong style="color:#f0fdf4;">Mixup + heavy transforms</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Inference</span><br><strong style="color:#f0fdf4;">TTA (7 augments averaged)</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Loss Function</span><br><strong style="color:#f0fdf4;">CrossEntropy + Label Smoothing</strong></div>
                    <div style="margin-top:8px;"><span style="color:rgba(220,252,231,0.35);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Classes / Target Acc</span><br><strong style="color:#4ade80;">38 diseases &nbsp;·&nbsp; 97%+ accuracy</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

#         st.markdown("""
#         <div class="result-card">
#             <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
#                  color:#4ade80;margin-bottom:14px;">🚀 Setup &amp; Deployment</div>
#         </div>
#         """, unsafe_allow_html=True)
#         st.code("""
# # 1. Install dependencies
# pip install -r requirements.txt

# # 2. Download PlantVillage dataset from Kaggle
# # https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
# # Place at: data/plantvillage/color/

# # 3. Train model (targets 97%+ accuracy)
# python model.py

# # 4. Run the app
# streamlit run app.py

# # 5. Deploy on Streamlit Cloud
# # → Push to GitHub → share.streamlit.io → Connect repo → Deploy
#         """, language="bash")


if __name__ == "__main__":
    main()