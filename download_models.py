import os
import gdown

def download_models():
    os.makedirs("models", exist_ok=True)

    files = {
        "models/best_weights.h5":  "1a-Wdh9hkesXZaM7NxIHsP5RqtBWsPeFP",
        "models/yield_model.pkl":  "1TMHG-c5u-HaWRih8vZydAu-NCvizgYVa",
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