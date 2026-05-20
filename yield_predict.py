# yield_predict.py
# Yield prediction logic for the ensemble model
# With rainfall (precipitation) and irrigation multipliers

import pickle
import json
import numpy as np
import os

MODEL_PATH    = "models/yield_model.pkl"
ENCODERS_PATH = "models/yield_encoders.pkl"
META_PATH     = "models/yield_meta.json"

_models   = None
_encoders = None
_meta     = None


# ─────────────────────────────────────────────
# VERIFIED BENCHMARK YIELDS (Kg/Ha)
# Source: Indian Council of Agricultural Research (ICAR)
# & Ministry of Agriculture, Government of India
# These are national average yields — state multipliers applied separately
# ─────────────────────────────────────────────
BENCHMARK_YIELDS_KG_HA = {
    # Cereals
    "Rice":               3100,   # national avg ~2200, UP avg ~2800, Punjab ~4000
    "Wheat":              3500,   # national avg ~3200, UP avg ~3500, Punjab ~4500
    "Maize":              2800,
    "Jowar":              1050,
    "Bajra":              1250,
    "Ragi":               1600,
    "Barley":             2500,
    "Small millets":       900,

    # Pulses
    "Arhar/Tur":           900,
    "Gram":               1100,
    "Moong(Green Gram)":   700,
    "Urad":                700,
    "Masoor":             1000,
    "Khesari":             800,
    "Cowpea(Lobia)":       800,
    "Moth":                600,
    "Horse-gram":          600,
    "Peas & beans (Pulses)": 900,
    "Other  Rabi pulses":   800,

    # Oilseeds
    "Groundnut":          1800,
    "Soyabean":           1200,
    "Sunflower":          1000,
    "Rapeseed &Mustard":  1200,
    "Sesamum":             450,
    "Linseed":             700,
    "Safflower":           900,
    "Niger seed":          500,
    "Castor seed":        1600,
    "Guar seed":           900,
    "Oilseeds total":     1100,

    # Cash crops
    "Sugarcane":         70000,   # Kg/Ha (70 tonnes/Ha national avg)
    "Cotton(lint)":       1800,   # lint only
    "Jute":               2400,
    "Mesta":              1800,
    "Sannhamp":           1500,
    "Tobacco":            1800,

    # Vegetables & Tubers
    "Potato":            22000,
    "Onion":             16000,
    "Garlic":            10000,
    "Sweet potato":       8000,
    "Tapioca":           25000,

    # Spices
    "Dry chillies":       1200,
    "Turmeric":           5000,   # fresh weight
    "Ginger":             8000,   # fresh weight
    "Coriander":           900,
    "Blackpepper":        1500,
    "Cardamom":            300,

    # Fruits & Plantation
    "Banana":            30000,
    "Coconut":            8000,   # Kg equivalent (copra basis)
    "Arecanut":           2500,
    "Cashewnut":           900,
}

# State-level yield multipliers relative to national average
# Based on ICAR & state agriculture department data
STATE_YIELD_MULTIPLIERS = {
    # High productivity states
    "Punjab":              1.35,
    "Haryana":             1.25,
    "Uttar Pradesh":       1.10,
    "Uttarakhand":         1.05,
    "Himachal Pradesh":    1.00,

    # Medium productivity
    "Andhra Pradesh":      1.05,
    "Telangana":           1.00,
    "Karnataka":           0.95,
    "Tamil Nadu":          1.00,
    "Kerala":              1.00,
    "Maharashtra":         0.95,
    "Gujarat":             1.00,
    "Madhya Pradesh":      0.90,
    "Chhattisgarh":        0.88,
    "Rajasthan":           0.85,

    # Lower productivity / hilly / NE states
    "Bihar":               0.92,
    "Jharkhand":           0.82,
    "Odisha":              0.88,
    "West Bengal":         1.05,
    "Assam":               0.85,
    "Manipur":             0.80,
    "Meghalaya":           0.78,
    "Mizoram":             0.75,
    "Nagaland":            0.75,
    "Sikkim":              0.80,
    "Tripura":             0.85,
    "Jammu and Kashmir":   0.88,
    "Goa":                 0.90,
    "Andaman and Nicobar Islands": 0.85,
}

# ─────────────────────────────────────────────
# CROP CLASSIFICATION
# ─────────────────────────────────────────────
KHARIF_CROPS = {
    "Rice", "Maize", "Jowar", "Bajra", "Cotton(lint)",
    "Groundnut", "Soyabean", "Arhar/Tur", "Moong(Green Gram)",
    "Urad", "Sugarcane", "Sesamum", "Cowpea(Lobia)",
    "Guar seed", "Moth", "Niger seed", "Sannhamp",
    "Turmeric", "Ginger", "Castor seed",
}

RABI_CROPS = {
    "Wheat", "Gram", "Barley", "Rapeseed &Mustard",
    "Linseed", "Masoor", "Peas & beans (Pulses)",
    "Coriander", "Safflower", "Other  Rabi pulses", "Khesari",
}

WHOLE_YEAR_CROPS = {
    "Banana", "Coconut", "Arecanut", "Blackpepper", "Cardamom",
    "Cashewnut", "Tapioca", "Sweet potato", "Potato", "Onion",
    "Garlic", "Dry chillies", "Tobacco", "Jute", "Mesta",
    "Oilseeds total", "Small millets", "Horse-gram", "Sunflower",
}


# ─────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────
def _load():
    global _models, _encoders, _meta
    if _models is None:
        with open(MODEL_PATH, "rb") as f:
            _models = pickle.load(f)
    if _encoders is None:
        with open(ENCODERS_PATH, "rb") as f:
            _encoders = pickle.load(f)
    if _meta is None:
        with open(META_PATH, "r") as f:
            _meta = json.load(f)


def is_model_ready():
    return (
        os.path.exists(MODEL_PATH) and
        os.path.exists(ENCODERS_PATH) and
        os.path.exists(META_PATH)
    )


def get_meta():
    _load()
    return _meta


# ─────────────────────────────────────────────
# STAT HELPERS
# ─────────────────────────────────────────────
def _get_crop_stat(crop, stat="mean"):
    for row in _meta.get("crop_stats", []):
        if row["crop"] == crop:
            return row.get(stat, 0) or 0
    return 0


def _get_state_mean(state):
    for row in _meta.get("state_stats", []):
        if row["state"] == state:
            return row.get("mean", 0) or 0
    return 0


def _get_crop_season_mean(crop, season):
    for row in _meta.get("crop_season_stats", []):
        if row["crop"] == crop and row["season"] == season:
            return row.get("mean", 0) or 0
    return 0


# ─────────────────────────────────────────────
# RAINFALL MULTIPLIER
# ─────────────────────────────────────────────
def _rainfall_factor(rainfall_mm, season, crop):
    """
    Returns a yield multiplier (0.0 – 1.10) based on annual rainfall.

    Logic:
    - Kharif crops are rain-fed → highly sensitive to rainfall
    - Rabi crops are irrigated  → low sensitivity to rainfall
    - Whole Year / perennial    → moderate sensitivity

    Values based on agronomic research and IMD rainfall-yield correlations.
    """
    # Determine effective season from crop if season is ambiguous
    effective_kharif = (season == "Kharif") or (crop in KHARIF_CROPS and season == "Whole Year")
    effective_rabi   = (season == "Rabi")   or (crop in RABI_CROPS   and season == "Whole Year")

    if effective_rabi:
        # Rabi is mostly irrigated — rainfall has very low impact
        # Only extreme dryness slightly hurts (less winter moisture)
        if rainfall_mm < 200:   return 0.88
        if rainfall_mm < 300:   return 0.93
        if rainfall_mm < 500:   return 0.97
        return 1.00  # sufficient winter moisture — no benefit from more rain

    elif effective_kharif:
        # Kharif is rain-fed — rainfall is the primary water source
        # Too little → drought stress; too much → waterlogging & disease
        if rainfall_mm < 300:   return 0.55   # severe drought
        if rainfall_mm < 500:   return 0.68   # drought stress
        if rainfall_mm < 700:   return 0.80   # below optimal
        if rainfall_mm < 900:   return 0.90   # slightly below optimal
        if rainfall_mm < 1100:  return 0.97   # near optimal
        if rainfall_mm < 1500:  return 1.00   # optimal for most Kharif
        if rainfall_mm < 2000:  return 0.98   # slightly excess
        if rainfall_mm < 2500:  return 0.94   # excess → waterlogging risk
        return 0.88                            # very excess → significant waterlogging

    elif season == "Summer":
        # Summer crops need supplemental water — moderate rain helps
        if rainfall_mm < 300:   return 0.80
        if rainfall_mm < 600:   return 0.90
        if rainfall_mm < 1000:  return 0.97
        return 1.00

    elif season == "Winter":
        # Winter crops sensitive to low rainfall (similar to Rabi)
        if rainfall_mm < 200:   return 0.88
        if rainfall_mm < 400:   return 0.94
        return 1.00

    else:
        # Whole Year / Autumn / perennial crops — moderate sensitivity
        if rainfall_mm < 400:   return 0.80
        if rainfall_mm < 700:   return 0.90
        if rainfall_mm < 1000:  return 0.96
        if rainfall_mm < 2000:  return 1.00
        if rainfall_mm < 3000:  return 0.97
        return 0.93


# ─────────────────────────────────────────────
# IRRIGATION MULTIPLIER
# ─────────────────────────────────────────────
def _irrigation_factor(irrigation_pct, season, crop):
    """
    Returns a yield multiplier (0.40 – 1.12) based on % of field under irrigation.

    irrigation_pct: 0–100
        0   = fully rain-fed (no canal/tubewell/drip)
        100 = fully irrigated

    Logic:
    - Rabi crops NEED irrigation to survive → very sensitive
    - Kharif crops use rain primarily → irrigation is supplemental
    - Whole Year / perennial crops benefit from consistent irrigation
    """
    ratio = irrigation_pct / 100.0  # normalise to 0–1

    effective_rabi   = (season == "Rabi")   or (crop in RABI_CROPS)
    effective_kharif = (season == "Kharif") or (crop in KHARIF_CROPS)

    if effective_rabi:
        # Rabi without irrigation = crop failure in most of India
        if ratio >= 0.90:   return 1.12   # fully irrigated → significant bonus
        if ratio >= 0.75:   return 1.05   # well irrigated
        if ratio >= 0.60:   return 1.00   # adequately irrigated
        if ratio >= 0.40:   return 0.85   # partially irrigated → yield drops
        if ratio >= 0.20:   return 0.68   # poorly irrigated
        if ratio >= 0.05:   return 0.52   # minimal irrigation
        return 0.40                        # no irrigation → near-crop failure

    elif effective_kharif:
        # Kharif relies on rain — irrigation is supplemental insurance
        if ratio >= 0.80:   return 1.07   # supplemental irrigation boosts yield
        if ratio >= 0.60:   return 1.04
        if ratio >= 0.40:   return 1.02
        if ratio >= 0.20:   return 1.00   # partial supplemental = normal
        if ratio >= 0.05:   return 0.98   # almost rain-fed
        return 0.95                        # fully rain-fed → slight risk

    elif season in ("Summer", "Winter"):
        # These short seasons need reliable water
        if ratio >= 0.80:   return 1.08
        if ratio >= 0.60:   return 1.03
        if ratio >= 0.40:   return 1.00
        if ratio >= 0.20:   return 0.88
        return 0.75

    else:
        # Whole Year / perennial crops (Banana, Sugarcane, Coconut etc.)
        if ratio >= 0.90:   return 1.10
        if ratio >= 0.70:   return 1.05
        if ratio >= 0.50:   return 1.00
        if ratio >= 0.30:   return 0.93
        if ratio >= 0.10:   return 0.85
        return 0.78


# ─────────────────────────────────────────────
# MAIN PREDICTION FUNCTION
# ─────────────────────────────────────────────
def predict_yield(crop, state, season, area,
                  annual_rainfall=1083,
                  irrigation_pct=50,
                  year=2024,
                  district=None):
    """
    Predict crop yield using the trained ensemble ML model,
    adjusted by rainfall and irrigation multipliers.

    Parameters
    ----------
    crop            : str   — crop name (e.g. "Rice")
    state           : str   — Indian state name
    season          : str   — "Kharif" | "Rabi" | "Whole Year" | "Summer" | "Winter" | "Autumn"
    area            : float — field area in hectares
    annual_rainfall : float — annual precipitation in mm (default: India avg 1083mm)
    irrigation_pct  : float — % of field under irrigation, 0–100 (default: 50%)
    year            : int   — crop year (default: 2024)
    district        : str   — optional district name

    Returns
    -------
    dict with keys:
        yield_per_ha       — raw ML prediction (Kg/Ha)
        adjusted_yield     — after rainfall + irrigation multipliers (Kg/Ha)
        total_production   — adjusted_yield × area (Kg)
        rainfall_factor    — multiplier applied for rainfall
        irrigation_factor  — multiplier applied for irrigation
        combined_factor    — rainfall_factor × irrigation_factor
        area, crop, state, season, annual_rainfall, irrigation_pct
    """
    _load()
    feature_cols = _meta["feature_cols"]
    row = {}

    # ── Encode categorical features ──
    for col in ["state", "season", "crop", "district"]:
        enc_col = col + "_enc"
        if enc_col in feature_cols:
            le  = _encoders[col]
            val = {
                "state":    state,
                "season":   season,
                "crop":     crop,
                "district": district or "",
            }.get(col, "")
            try:
                row[enc_col] = le.transform([str(val).strip().title()])[0]
            except ValueError:
                row[enc_col] = 0

    # ── Numeric features ──
    if "area"             in feature_cols: row["area"]             = float(area)
    if "log_area"         in feature_cols: row["log_area"]         = float(np.log1p(area))
    if "year"             in feature_cols: row["year"]             = int(year)
    if "crop_mean_yield"  in feature_cols: row["crop_mean_yield"]  = _get_crop_stat(crop, "mean")
    if "crop_median_yield"in feature_cols: row["crop_median_yield"]= _get_crop_stat(crop, "median")
    if "crop_std_yield"   in feature_cols: row["crop_std_yield"]   = _get_crop_stat(crop, "std")
    if "state_mean_yield" in feature_cols: row["state_mean_yield"] = _get_state_mean(state)
    if "crop_season_mean" in feature_cols: row["crop_season_mean"] = _get_crop_season_mean(crop, season)

    X = np.array([[row.get(c, 0) for c in feature_cols]])

    # ── Ensemble / single model prediction ──
    if isinstance(_models, dict):
        preds        = [m.predict(X)[0] for m in _models.values()]
        yield_per_ha = float(np.mean(preds))
    else:
        yield_per_ha = float(_models.predict(X)[0])

    yield_per_ha = max(0.01, yield_per_ha)

    # ── Sanity check: compare ML prediction vs known benchmark ──
    benchmark_kg_ha  = BENCHMARK_YIELDS_KG_HA.get(crop)
    state_multiplier = STATE_YIELD_MULTIPLIERS.get(state, 1.0)

    if benchmark_kg_ha is not None:
        expected_kg_ha = benchmark_kg_ha * state_multiplier

        # If ML prediction is less than 5% of benchmark → model is clearly wrong
        # Use benchmark instead and blend slightly with ML
        if yield_per_ha < expected_kg_ha * 0.05:
            # ML gave garbage (e.g. 1 Kg/Ha for wheat) — use benchmark directly
            yield_per_ha = expected_kg_ha
            prediction_source = "benchmark"

        elif yield_per_ha < expected_kg_ha * 0.30:
            # ML is very low but not impossible — blend 80% benchmark + 20% ML
            yield_per_ha = (expected_kg_ha * 0.80) + (yield_per_ha * 0.20)
            prediction_source = "blended"

        elif yield_per_ha > expected_kg_ha * 5.0:
            # ML is absurdly high — cap at 2× benchmark
            yield_per_ha = expected_kg_ha * 2.0
            prediction_source = "capped"

        else:
            # ML prediction is in a reasonable range — trust it
            prediction_source = "ml"
    else:
        expected_kg_ha    = yield_per_ha
        prediction_source = "ml"

    # ── Apply rainfall and irrigation multipliers ──
    rf_factor  = _rainfall_factor(annual_rainfall, season, crop)
    irr_factor = _irrigation_factor(irrigation_pct, season, crop)
    combined   = rf_factor * irr_factor

    adjusted_yield   = yield_per_ha * combined
    adjusted_yield   = max(1.0, adjusted_yield)
    total_production = adjusted_yield * float(area)

    return {
        "yield_per_ha":        round(yield_per_ha, 2),
        "adjusted_yield":      round(adjusted_yield, 2),
        "total_production":    round(total_production, 2),
        "rainfall_factor":     round(rf_factor, 3),
        "irrigation_factor":   round(irr_factor, 3),
        "combined_factor":     round(combined, 3),
        "expected_kg_ha":      round(expected_kg_ha, 2),
        "state_multiplier":    round(state_multiplier, 3),
        "prediction_source":   prediction_source,
        "area":                float(area),
        "crop":                crop,
        "state":               state,
        "season":              season,
        "annual_rainfall":     annual_rainfall,
        "irrigation_pct":      irrigation_pct,
    }


# ─────────────────────────────────────────────
# RECOMMENDATIONS
# ─────────────────────────────────────────────
def get_recommendations(result):
    """
    Generate agronomic recommendations based on prediction result.
    Now accounts for rainfall and irrigation levels.
    """
    crop           = result["crop"]
    yield_val      = result["adjusted_yield"]
    season         = result["season"]
    rainfall       = result.get("annual_rainfall", 1083)
    irrigation_pct = result.get("irrigation_pct", 50)
    rf_factor      = result.get("rainfall_factor", 1.0)
    irr_factor     = result.get("irrigation_factor", 1.0)

    benchmarks = {
        "Rice": 2.5, "Wheat": 3.0, "Maize": 2.8, "Cotton(lint)": 1.5,
        "Sugarcane": 65.0, "Soyabean": 1.2, "Groundnut": 1.5,
        "Bajra": 1.2, "Jowar": 1.0, "Ragi": 1.5, "Sunflower": 1.0,
        "Potato": 20.0, "Onion": 15.0, "Banana": 30.0,
        "Moong(Green Gram)": 0.7, "Urad": 0.7, "Arhar/Tur": 0.9,
        "Gram": 1.1, "Rapeseed &Mustard": 1.2, "Linseed": 0.7,
        "Castor seed": 1.5, "Sesamum": 0.4,
    }

    _load()
    benchmark = benchmarks.get(
        crop,
        _get_crop_stat(crop, "mean") or yield_val * 0.9
    )
    ratio = yield_val / benchmark if benchmark > 0 else 1.0

    # ── Performance tier ──
    if ratio >= 1.2:
        performance = "🌟 Excellent"
        recs = [
            f"Predicted yield of {yield_val:.2f} t/ha is well above average for {crop}.",
            "Maintain your current soil health and irrigation practices.",
            "Consider storing surplus or exploring export/mandi markets.",
            "Document your practices this season — they are working well!",
        ]
    elif ratio >= 0.9:
        performance = "✅ Good"
        recs = [
            f"Predicted yield of {yield_val:.2f} t/ha is near the national average for {crop}.",
            "Soil testing every season helps fine-tune fertilizer use.",
            "Ensure timely irrigation especially during flowering stage.",
            "Use certified seeds from a reliable source next season.",
        ]
    elif ratio >= 0.6:
        performance = "⚠️ Below Average"
        recs = [
            f"Predicted yield of {yield_val:.2f} t/ha is below average for {crop} (avg: {benchmark:.2f} t/ha).",
            "Get a soil health card test — low NPK is a common cause.",
            "Check for pest/disease pressure and consult a local agronomist.",
            "Improve field drainage if waterlogging is an issue.",
            "Consider switching to high-yielding variety (HYV) seeds.",
        ]
    else:
        performance = "🚨 Poor — Action Needed"
        recs = [
            f"Yield of {yield_val:.2f} t/ha is significantly below average for {crop}.",
            "Urgent soil health check recommended.",
            "Review irrigation — both under and over watering reduce yield.",
            "Contact your nearest Krishi Vigyan Kendra (KVK) for expert guidance.",
            "Consider crop insurance to protect against future losses.",
        ]

    # ── Rainfall-specific advice ──
    rain_advice = []
    if rf_factor < 0.80:
        rain_advice.append(
            f"⚠️ Low rainfall ({rainfall:.0f}mm) is significantly reducing your yield. "
            "Consider drip/sprinkler irrigation to compensate."
        )
    elif rf_factor < 0.95:
        rain_advice.append(
            f"🌧️ Rainfall ({rainfall:.0f}mm) is slightly below optimal. "
            "Supplement with irrigation during critical growth stages."
        )
    elif rf_factor <= 0.97 and rainfall > 2000:
        rain_advice.append(
            f"💧 Very high rainfall ({rainfall:.0f}mm) may cause waterlogging. "
            "Ensure proper field drainage channels are in place."
        )

    # ── Irrigation-specific advice ──
    irr_advice = []
    if irr_factor < 0.70:
        irr_advice.append(
            f"🚿 Very low irrigation coverage ({irrigation_pct:.0f}%) is a major yield limiter. "
            "Even a basic drip system can boost yield by 30–40%."
        )
    elif irr_factor < 0.90:
        irr_advice.append(
            f"💧 Irrigation at {irrigation_pct:.0f}% — consider expanding coverage "
            "especially during flowering and grain-filling stages."
        )
    elif irr_factor >= 1.08:
        irr_advice.append(
            f"✅ Excellent irrigation coverage ({irrigation_pct:.0f}%) — "
            "your field has optimal water management."
        )

    # ── Season tip ──
    season_tips = {
        "Kharif":     "Kharif crops need good monsoon — ensure water conservation bunds.",
        "Rabi":       "Rabi crops depend on irrigation — check canal/groundwater availability.",
        "Whole Year": "Year-round cultivation needs consistent soil nutrition management.",
        "Summer":     "Summer crops need extra irrigation and heat-tolerant varieties.",
        "Winter":     "Winter crops benefit from cool temperatures — protect from frost.",
        "Autumn":     "Autumn crops need well-drained soil and timely sowing.",
    }

    return {
        "performance":      performance,
        "benchmark":        benchmark,
        "recommendations":  recs,
        "rain_advice":      rain_advice,
        "irr_advice":       irr_advice,
        "season_tip":       season_tips.get(season, ""),
    }