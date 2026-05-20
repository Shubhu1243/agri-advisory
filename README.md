# 🌿 AgriDoc — Intelligent Agri Advisory System

A machine learning project that detects plant diseases from leaf photos and recommends pesticides.
Built with TensorFlow, MobileNetV2, and Streamlit.

---

## 📁 Project Structure

```
agri_advisory/
├── app.py              # Main Streamlit UI (run this)
├── model.py            # Train the ML model (run once)
├── predict.py          # Image preprocessing & inference
├── disease_info.py     # Disease + pesticide database
├── requirements.txt    # Python dependencies
├── README.md           # This file
│
├── data/               # (Create this) Put dataset here
│   └── plantvillage/   # Downloaded from Kaggle
│
└── models/             # (Auto-created) Saved model files
    ├── plant_disease_model.h5
    └── class_names.txt
```

---

## 🚀 Setup Instructions

### Step 1 — Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Download the Dataset
Download **PlantVillage Dataset** from Kaggle:
🔗 https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset

Create the folder and place the dataset:
```
data/
└── plantvillage/
    ├── Apple___Apple_scab/
    ├── Apple___Black_rot/
    ├── Tomato___Early_blight/
    └── ... (38 folders total)
```

### Step 3 — Train the Model
```bash
python model.py
```
- Training takes **1-3 hours** on CPU, ~20 mins on GPU
- Model is saved to `models/plant_disease_model.h5`
- Class names saved to `models/class_names.txt`

### Step 4 — Run the App
```bash
streamlit run app.py
```

Open in browser: `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push your code to **GitHub** (exclude `data/` and `models/` folders)
2. Train the model and upload `models/` folder to GitHub (or use Git LFS)
3. Go to: https://share.streamlit.io
4. Click **New App** → Connect your GitHub repo
5. Set **Main file path**: `app.py`
6. Click **Deploy**!

> **Note:** For Streamlit Cloud deployment, add a `models/` folder with your trained model.
> If model is too large for GitHub, use Git LFS or upload to Google Drive and download at startup.

---

## 🧠 Model Details

| Property | Value |
|----------|-------|
| Architecture | MobileNetV2 (Transfer Learning) |
| Input Size | 224 × 224 × 3 |
| Output Classes | 38 diseases |
| Dataset | PlantVillage (54,306 images) |
| Training Strategy | 2-phase (frozen → fine-tune) |
| Expected Accuracy | ~94-96% |
| Model Size | ~14 MB |

---

## 🌾 Supported Crops & Diseases

| Crop | Diseases Covered |
|------|-----------------|
| 🍎 Apple | Apple Scab, Black Rot, Cedar Rust |
| 🍅 Tomato | Early Blight, Late Blight, YLCV, Bacterial Spot, etc. |
| 🥔 Potato | Early Blight, Late Blight |
| 🌽 Corn | Common Rust, Gray Leaf Spot, Northern Blight |
| 🍇 Grape | Black Rot, Esca, Leaf Blight |
| 🍑 Peach | Bacterial Spot |
| 🍓 Strawberry | Leaf Scorch |
| 🫑 Pepper | Bacterial Spot |
| 🍊 Orange | Huanglongbing (Citrus Greening) |

---

## 💡 Features

- ✅ **Photo Upload** — Upload or capture leaf photo
- ✅ **Disease Detection** — AI identifies disease with confidence score
- ✅ **Top 5 Predictions** — See alternative diagnoses
- ✅ **Pesticide Guide** — Top 5 pesticides with dosage & frequency
- ✅ **Symptom List** — Know what to look for
- ✅ **Prevention Tips** — Stop disease before it spreads
- ✅ **Disease Library** — Browse all supported diseases
- ✅ **Report Download** — Export diagnosis as text file
- ✅ **Demo Mode** — Works without model for UI testing
- ✅ **Farmer-Friendly UI** — Simple, bilingual-ready interface

---

## 📞 Help & Resources

- **Kisan Call Center:** 1800-180-1551 (Free, 24x7)
- **Kaggle Dataset:** https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- **Streamlit Docs:** https://docs.streamlit.io
- **TensorFlow Docs:** https://www.tensorflow.org

---

*Built for College Project — Intelligent Agri Advisory System*