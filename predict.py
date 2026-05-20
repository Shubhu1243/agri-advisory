# predict.py
# Handles image preprocessing and model inference with TTA support

import os
import numpy as np
from PIL import Image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
try:
    import tensorflow as tf
except ImportError:
    import tf_keras as tf

SAVED_MODEL_PATH = "models/saved_model"
WEIGHTS_PATH     = "models/best_weights.h5"
CLASS_NAMES_PATH = "models/class_names.txt"
IMAGE_SIZE       = (224, 224)

DEMO_CLASS_NAMES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust",
    "Apple___healthy", "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_", "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy", "Grape___Black_rot", "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot",
    "Peach___healthy", "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot",
    "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
]


def load_class_names() -> list:
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r") as f:
            names = [l.strip() for l in f if l.strip()]
        if len(names) >= 10:
            return names
    return DEMO_CLASS_NAMES


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess image using EfficientNet's preprocess_input.
    EfficientNet expects pixel values in [0,255] range — NOT /255 normalized.
    """
    from tensorflow.keras.applications.efficientnet import preprocess_input
    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE, Image.LANCZOS)
    arr = np.array(image, dtype=np.float32)
    arr = preprocess_input(arr)          # ← KEY: EfficientNet preprocessing
    return np.expand_dims(arr, axis=0)


def augment_image(image: Image.Image, seed: int) -> np.ndarray:
    """
    Apply random augmentation for Test Time Augmentation (TTA).
    Uses EfficientNet preprocessing — NOT /255 normalization.
    """
    from tensorflow.keras.applications.efficientnet import preprocess_input
    from PIL import ImageEnhance
    import random

    random.seed(seed)
    np.random.seed(seed)

    img = image.convert("RGB")

    # Random horizontal flip
    if random.random() > 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    # Random rotation ±15 degrees
    angle = random.uniform(-15, 15)
    img = img.rotate(angle, fillcolor=(0, 0, 0))

    # Random brightness
    factor = random.uniform(0.85, 1.15)
    img = ImageEnhance.Brightness(img).enhance(factor)

    # Random zoom
    zoom = random.uniform(0.90, 1.0)
    w, h = img.size
    left = int(w * (1 - zoom) / 2)
    top = int(h * (1 - zoom) / 2)
    right = w - left
    bottom = h - top
    img = img.crop((left, top, right, bottom))
    img = img.resize(IMAGE_SIZE, Image.LANCZOS)

    arr = np.array(img, dtype=np.float32)
    arr = preprocess_input(arr)          # ← KEY: EfficientNet preprocessing
    return np.expand_dims(arr, axis=0)


def build_keras_model():
    """Rebuild model architecture and load weights."""
    from tensorflow.keras.applications import EfficientNetB3
    from tensorflow.keras.applications.efficientnet import preprocess_input
    from tensorflow.keras.layers import (
        Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    )
    from tensorflow.keras.models import Model
    from tensorflow.keras.regularizers import l2

    base_model = EfficientNetB3(
        weights="imagenet",
        include_top=False,
        input_shape=(*IMAGE_SIZE, 3)
    )
    inputs = base_model.input
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    x = Dense(256, activation="relu", kernel_regularizer=l2(1e-4))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    outputs = Dense(38, activation="softmax")(x)
    model = Model(inputs=inputs, outputs=outputs)
    return model


def load_model():
    """
    Load model — tries saved_model first, then weights fallback.
    """
    # Option 1: Load from saved_model folder
    if os.path.exists(SAVED_MODEL_PATH):
        try:
            model = tf.keras.models.load_model(SAVED_MODEL_PATH)
            print("✅ Loaded model from saved_model")
            return model
        except Exception as e:
            print(f"saved_model load failed: {e}")

    # Option 2: Rebuild architecture + load weights
    if os.path.exists(WEIGHTS_PATH):
        try:
            model = build_keras_model()
            model.load_weights(WEIGHTS_PATH)
            print("✅ Loaded model from weights")
            return model
        except Exception as e:
            print(f"Weights load failed: {e}")

    return None


def run_inference(model, preprocessed: np.ndarray) -> np.ndarray:
    """
    Run inference — handles both Keras model and SavedModel.
    """
    try:
        # Standard Keras model
        return model.predict(preprocessed, verbose=0)[0]
    except Exception:
        try:
            # TF SavedModel format
            infer = model.signatures["serving_default"]
            input_name = list(infer.structured_input_signature[1].keys())[0]
            output = infer(**{input_name: tf.constant(preprocessed)})
            output_key = list(output.keys())[0]
            return output[output_key].numpy()[0]
        except Exception as e:
            print(f"Inference error: {e}")
            return np.ones(38) / 38  # uniform fallback


def predict_disease(image: Image.Image, model=None, use_tta: bool = True,
                    tta_steps: int = 7) -> dict:
    """
    Run inference with optional Test Time Augmentation.
    TTA averages predictions over multiple augmented versions.
    """
    class_names = load_class_names()
    demo_mode = False

    if model is None:
        demo_mode = True
        num_classes = len(class_names)
        np.random.seed(abs(hash(image.tobytes()[:50])) % (2**31))
        probs = np.random.dirichlet(np.ones(num_classes) * 0.05)
        top_idx = np.random.randint(0, num_classes)
        probs[top_idx] += 5.0
        probs = probs / probs.sum()
    else:
        if use_tta:
            all_probs = []

            # Original image
            orig = preprocess_image(image)
            all_probs.append(run_inference(model, orig))

            # Augmented versions
            for seed in range(tta_steps - 1):
                aug = augment_image(image, seed=seed * 7)
                all_probs.append(run_inference(model, aug))

            probs = np.mean(all_probs, axis=0)
        else:
            preprocessed = preprocess_image(image)
            probs = run_inference(model, preprocessed)

    # Top 5 predictions
    top5_idx = np.argsort(probs)[::-1][:5]
    top_predictions = [
        (class_names[i], float(probs[i]) * 100)
        for i in top5_idx
    ]

    return {
        "predicted_class": top_predictions[0][0],
        "confidence": top_predictions[0][1],
        "top_predictions": top_predictions,
        "demo_mode": demo_mode,
        "tta_used": use_tta and model is not None,
        "class_names": class_names
    }


def format_class_name(raw_name: str) -> str:
    parts = raw_name.split("___")
    if len(parts) == 2:
        return f"{parts[0].replace('_',' ').strip()} – {parts[1].replace('_',' ').strip()}"
    return raw_name.replace("_", " ")