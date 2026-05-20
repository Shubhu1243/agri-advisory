import os
import gdown

def download_models():
    os.makedirs("models", exist_ok=True)

    files = {
        "models/best_weights.h5":  "YOUR_BEST_WEIGHTS_FILE_ID",
        "models/yield_model.pkl":  "YOUR_YIELD_MODEL_FILE_ID",
    }

    for path, file_id in files.items():
        if not os.path.exists(path):
            print(f"Downloading {path}...")
            gdown.download(
                f"https://drive.google.com/uc?id={file_id}",
                path,
                quiet=False
            )
            print(f"✅ {path} downloaded!")
        else:
            print(f"✅ {path} already exists, skipping.")

if __name__ == "__main__":
    download_models()