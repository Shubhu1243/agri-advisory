# yield_model.py
# Crop Yield Prediction — Improved Model
# Uses GradientBoostingRegressor + feature engineering for better accuracy
#
# Dataset: Crop Production in India
# Download: https://www.kaggle.com/datasets/abhinand05/crop-production-in-india
# Place at: data/crop_production.csv

import os
import numpy as np
import pandas as pd
import pickle
import json
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
DATASET_PATH  = "data/crop_production.csv"
MODEL_PATH    = "models/yield_model.pkl"
ENCODERS_PATH = "models/yield_encoders.pkl"
META_PATH     = "models/yield_meta.json"


# ─────────────────────────────────────────────
# LOAD & CLEAN
# ─────────────────────────────────────────────
def load_and_clean(path):
    print("📂 Loading dataset...")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    rename_map = {}
    for col in df.columns:
        if "state" in col:               rename_map[col] = "state"
        if "district" in col:            rename_map[col] = "district"
        if "crop_year" in col or col == "year": rename_map[col] = "year"
        if "season" in col:              rename_map[col] = "season"
        if col == "crop":                rename_map[col] = "crop"
        if "area" in col:                rename_map[col] = "area"
        if "production" in col:          rename_map[col] = "production"
    df.rename(columns=rename_map, inplace=True)

    df.dropna(subset=["production", "area"], inplace=True)
    df = df[(df["area"] > 0) & (df["production"] > 0)]

    # Yield in tonnes/hectare
    df["yield"] = df["production"] / df["area"]

    # Remove bottom 0.5% and top 1% outliers for cleaner training
    q_low  = df["yield"].quantile(0.005)
    q_high = df["yield"].quantile(0.99)
    df = df[(df["yield"] >= q_low) & (df["yield"] <= q_high)]

    # Clean strings
    for col in ["state", "season", "crop", "district"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    print(f"   Clean shape : {df.shape}")
    print(f"   Crops       : {df['crop'].nunique()}")
    print(f"   States      : {df['state'].nunique()}")
    print(f"   Yield range : {df['yield'].min():.2f} – {df['yield'].max():.2f} t/ha")
    return df


# ─────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────
def prepare_features(df):
    print("\n🔧 Engineering features...")

    encoders = {}
    cat_cols = ["state", "season", "crop"]
    if "district" in df.columns:
        cat_cols.append("district")

    for col in cat_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col + "_enc"] = le.fit_transform(df[col])
            encoders[col] = le

    # ── Crop-level statistics (powerful feature) ──
    crop_stats = df.groupby("crop")["yield"].agg(["mean", "median", "std"]).reset_index()
    crop_stats.columns = ["crop", "crop_mean_yield", "crop_median_yield", "crop_std_yield"]
    df = df.merge(crop_stats, on="crop", how="left")

    # State-level statistics
    state_stats = df.groupby("state")["yield"].agg(["mean"]).reset_index()
    state_stats.columns = ["state", "state_mean_yield"]
    df = df.merge(state_stats, on="state", how="left")

    # Crop-Season interaction mean
    cs_stats = df.groupby(["crop", "season"])["yield"].mean().reset_index()
    cs_stats.columns = ["crop", "season", "crop_season_mean"]
    df = df.merge(cs_stats, on=["crop", "season"], how="left")

    # Log area (reduces skewness)
    df["log_area"] = np.log1p(df["area"])

    feature_cols = (
        [c + "_enc" for c in cat_cols if c in df.columns] +
        ["area", "log_area", "crop_mean_yield", "crop_median_yield",
         "crop_std_yield", "state_mean_yield", "crop_season_mean"]
    )
    if "year" in df.columns:
        feature_cols.append("year")

    df[feature_cols] = df[feature_cols].fillna(0)

    X = df[feature_cols].values
    y = df["yield"].values

    print(f"   Features : {feature_cols}")
    print(f"   Samples  : {len(X)}")
    return X, y, encoders, feature_cols, df


# ─────────────────────────────────────────────
# TRAIN MODEL
# ─────────────────────────────────────────────
def train_model(X, y):
    print("\n🌲 Training models...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Random Forest
    print("   Training Random Forest...")
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=25,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_r2  = r2_score(y_test, rf_pred)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    print(f"   RF  → R²: {rf_r2:.4f} | MAE: {rf_mae:.4f}")

    # Gradient Boosting
    print("   Training Gradient Boosting...")
    gb = GradientBoostingRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_split=5,
        random_state=42
    )
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)
    gb_r2  = r2_score(y_test, gb_pred)
    gb_mae = mean_absolute_error(y_test, gb_pred)
    print(f"   GB  → R²: {gb_r2:.4f} | MAE: {gb_mae:.4f}")

    # Ensemble: average of both
    ens_pred = (rf_pred + gb_pred) / 2
    ens_r2   = r2_score(y_test, ens_pred)
    ens_mae  = mean_absolute_error(y_test, ens_pred)
    print(f"   ENS → R²: {ens_r2:.4f} | MAE: {ens_mae:.4f} ✅ (Ensemble)")

    return {"rf": rf, "gb": gb}, ens_r2, ens_mae


# ─────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────
def save_artifacts(models, encoders, feature_cols, df, r2, mae):
    os.makedirs("models", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(models, f)
    print(f"\n💾 Model saved     → {MODEL_PATH}")

    with open(ENCODERS_PATH, "wb") as f:
        pickle.dump(encoders, f)
    print(f"💾 Encoders saved  → {ENCODERS_PATH}")

    # Crop stats for prediction
    crop_stats = df.groupby("crop")["yield"].agg(["mean", "median", "std"]).reset_index()
    crop_stats.columns = ["crop", "mean", "median", "std"]

    state_stats = df.groupby("state")["yield"].mean().reset_index()
    state_stats.columns = ["state", "mean"]

    cs_stats = df.groupby(["crop", "season"])["yield"].mean().reset_index()
    cs_stats.columns = ["crop", "season", "mean"]

    meta = {
        "feature_cols":   feature_cols,
        "r2_score":       round(r2, 4),
        "mae":            round(mae, 4),
        "crops":          sorted(df["crop"].unique().tolist()),
        "states":         sorted(df["state"].unique().tolist()),
        "seasons":        sorted(df["season"].unique().tolist()),
        "crop_stats":     crop_stats.fillna(0).to_dict(orient="records"),
        "state_stats":    state_stats.fillna(0).to_dict(orient="records"),
        "crop_season_stats": cs_stats.fillna(0).to_dict(orient="records"),
    }
    if "district" in df.columns:
        meta["districts"] = sorted(df["district"].unique().tolist())

    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"💾 Metadata saved  → {META_PATH}")
    print(f"\n📋 Crops    : {len(meta['crops'])}")
    print(f"📋 States   : {len(meta['states'])}")
    print(f"📋 Seasons  : {len(meta['seasons'])}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  🌾 Crop Yield Prediction — Model Training (Improved)")
    print("=" * 60)

    if not os.path.exists(DATASET_PATH):
        print(f"\n❌ Dataset not found: {DATASET_PATH}")
        print("📥 https://www.kaggle.com/datasets/abhinand05/crop-production-in-india")
        return

    df = load_and_clean(DATASET_PATH)
    X, y, encoders, feature_cols, df = prepare_features(df)
    models, r2, mae = train_model(X, y)
    save_artifacts(models, encoders, feature_cols, df, r2, mae)

    print("\n" + "=" * 60)
    print("  🎉 TRAINING COMPLETE!")
    print(f"  🎯 Ensemble R² : {r2:.4f}")
    print(f"  🎯 Ensemble MAE: {mae:.4f} t/ha")
    print(f"\n  Now run: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()