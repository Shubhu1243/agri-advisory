# model.py
# OPTIMIZED FOR 97%+ ACCURACY
# EfficientNetB3 + 3-Phase Training + TTA
# KEY FIX: Using EfficientNet's own preprocess_input instead of /255

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import (
    Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
)
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from sklearn.utils.class_weight import compute_class_weight
import json

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
DATASET_PATH     = "data/plantvillage/color"
MODEL_SAVE_PATH  = "models/plant_disease_model.h5"
WEIGHTS_PATH     = "models/best_weights.h5"
CLASS_NAMES_PATH = "models/class_names.txt"
LOGS_DIR         = "logs"
IMAGE_SIZE       = (224, 224)
BATCH_SIZE       = 32
EPOCHS_PHASE1    = 20
EPOCHS_PHASE2    = 20
EPOCHS_PHASE3    = 10
BASE_LR          = 1e-3
VALIDATION_SPLIT = 0.15
L2_REG           = 1e-4


# ─────────────────────────────────────────────
# SAFE MODEL CHECKPOINT
# ─────────────────────────────────────────────
class SafeModelCheckpoint(tf.keras.callbacks.Callback):
    def __init__(self, weights_path, monitor="val_accuracy", mode="max", verbose=1):
        super().__init__()
        self.weights_path = weights_path
        self.monitor = monitor
        self.verbose = verbose
        self.best = -np.inf if mode == "max" else np.inf
        self.mode = mode

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        raw = logs.get(self.monitor, None)
        if raw is None:
            return
        current = float(raw.numpy()) if hasattr(raw, 'numpy') else float(raw)
        improved = (current > self.best) if self.mode == "max" else (current < self.best)
        if improved:
            if self.verbose:
                print(f"\nEpoch {epoch+1}: {self.monitor} improved "
                      f"from {self.best:.5f} to {current:.5f}, "
                      f"saving weights to {self.weights_path}")
            self.best = current
            self.model.save_weights(self.weights_path)


# ─────────────────────────────────────────────
# MODEL BUILDING
# ─────────────────────────────────────────────
def build_model(num_classes: int):
    base_model = EfficientNetB3(
        weights="imagenet",
        include_top=False,
        input_shape=(*IMAGE_SIZE, 3)
    )
    base_model.trainable = False

    inputs = base_model.input
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    x = Dense(256, activation="relu", kernel_regularizer=l2(L2_REG))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model, base_model


# ─────────────────────────────────────────────
# DATA GENERATORS
# KEY FIX: preprocess_input instead of rescale=1/255
# EfficientNet expects pixel values in range [0, 255]
# and applies its own normalization internally
# ─────────────────────────────────────────────
def get_generators():
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,  # ← KEY FIX
        validation_split=VALIDATION_SPLIT,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode="nearest"
    )

    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,  # ← KEY FIX
        validation_split=VALIDATION_SPLIT
    )

    train_gen = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
        shuffle=True,
        seed=42
    )

    val_gen = val_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
        seed=42
    )

    return train_gen, val_gen


# ─────────────────────────────────────────────
# CLASS WEIGHTS
# ─────────────────────────────────────────────
def get_class_weights(train_gen):
    classes = train_gen.classes
    unique_classes = np.unique(classes)
    weights = compute_class_weight(
        class_weight="balanced",
        classes=unique_classes,
        y=classes
    )
    return dict(zip(unique_classes, weights))


# ─────────────────────────────────────────────
# SAVE CLASS NAMES
# ─────────────────────────────────────────────
def save_class_names(generator):
    os.makedirs("models", exist_ok=True)
    index_to_class = {v: k for k, v in generator.class_indices.items()}
    class_names = [index_to_class[i] for i in range(len(index_to_class))]
    with open(CLASS_NAMES_PATH, "w") as f:
        for name in class_names:
            f.write(name + "\n")
    print(f"✅ Saved {len(class_names)} class names")
    print(f"   Sample: {class_names[:4]}")
    return class_names


# ─────────────────────────────────────────────
# CALLBACKS
# ─────────────────────────────────────────────
def get_callbacks(patience_early=8, patience_lr=4):
    os.makedirs(LOGS_DIR, exist_ok=True)
    return [
        SafeModelCheckpoint(
            WEIGHTS_PATH,
            monitor="val_accuracy",
            mode="max",
            verbose=1
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=patience_early,
            restore_best_weights=True,
            verbose=1,
            mode="max"
        ),
        ReduceLROnPlateau(
            monitor="val_accuracy",
            factor=0.5,
            patience=patience_lr,
            min_lr=1e-8,
            verbose=1,
            mode="max"
        ),
    ]


# ─────────────────────────────────────────────
# PHASE 1 — Train head only, base FROZEN
# ─────────────────────────────────────────────
def phase1_train(model, train_gen, val_gen, class_weights):
    print("\n" + "="*60)
    print("🚀 PHASE 1: Training classification head")
    print(f"   Base model: FROZEN | LR: {BASE_LR}")
    print("="*60)

    model.compile(
        optimizer=Adam(learning_rate=BASE_LR),
        loss="categorical_crossentropy",
        metrics=["accuracy",
                 tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")]
    )

    return model.fit(
        train_gen,
        epochs=EPOCHS_PHASE1,
        validation_data=val_gen,
        callbacks=get_callbacks(patience_early=8, patience_lr=4),
        class_weight=class_weights,
        verbose=1
    )


# ─────────────────────────────────────────────
# PHASE 2 — Unfreeze top 80 layers
# ─────────────────────────────────────────────
def phase2_train(model, base_model, train_gen, val_gen, class_weights):
    print("\n" + "="*60)
    print("🔧 PHASE 2: Fine-tuning top 80 layers")
    print(f"   LR: {BASE_LR / 10}")
    print("="*60)

    base_model.trainable = True
    for layer in base_model.layers[:-80]:
        layer.trainable = False

    trainable = sum(1 for l in model.layers if l.trainable)
    print(f"   Trainable layers: {trainable}")

    model.compile(
        optimizer=Adam(learning_rate=BASE_LR / 10),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=["accuracy",
                 tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")]
    )

    return model.fit(
        train_gen,
        epochs=EPOCHS_PHASE2,
        validation_data=val_gen,
        callbacks=get_callbacks(patience_early=8, patience_lr=4),
        class_weight=class_weights,
        verbose=1
    )


# ─────────────────────────────────────────────
# PHASE 3 — Unfreeze ALL layers
# ─────────────────────────────────────────────
def phase3_train(model, base_model, train_gen, val_gen, class_weights):
    print("\n" + "="*60)
    print("✨ PHASE 3: Full model fine-tuning")
    print(f"   LR: {BASE_LR / 100}")
    print("="*60)

    base_model.trainable = True

    model.compile(
        optimizer=Adam(learning_rate=BASE_LR / 100),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy",
                 tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")]
    )

    return model.fit(
        train_gen,
        epochs=EPOCHS_PHASE3,
        validation_data=val_gen,
        callbacks=get_callbacks(patience_early=6, patience_lr=3),
        class_weight=class_weights,
        verbose=1
    )


# ─────────────────────────────────────────────
# TEST TIME AUGMENTATION (TTA)
# ─────────────────────────────────────────────
def evaluate_with_tta(model, n_augments=5):
    print(f"\n📊 Evaluating with TTA (x{n_augments} augmentations)...")

    tta_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=10,
        horizontal_flip=True,
        zoom_range=0.1,
        brightness_range=[0.9, 1.1]
    )

    clean_gen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=VALIDATION_SPLIT
    )
    true_gen = clean_gen.flow_from_directory(
        DATASET_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
        seed=42
    )
    true_labels = true_gen.classes

    all_preds = []
    for i in range(n_augments):
        tta_gen = tta_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset="validation",
            shuffle=False,
            seed=i * 7
        )
        preds = model.predict(tta_gen, verbose=0)
        all_preds.append(preds)

    avg_preds = np.mean(all_preds, axis=0)
    predicted_classes = np.argmax(avg_preds, axis=1)
    tta_accuracy = np.mean(predicted_classes == true_labels)
    print(f"   ✅ TTA Accuracy: {tta_accuracy * 100:.2f}%")
    return float(tta_accuracy)


# ─────────────────────────────────────────────
# SAVE TRAINING SUMMARY
# ─────────────────────────────────────────────
def save_training_summary(val_acc, tta_acc, num_classes):
    summary = {
        "model": "EfficientNetB3",
        "num_classes": int(num_classes),
        "image_size": list(IMAGE_SIZE),
        "val_accuracy": round(float(val_acc) * 100, 2),
        "tta_accuracy": round(float(tta_acc) * 100, 2),
        "batch_size": BATCH_SIZE,
        "dataset_path": DATASET_PATH
    }
    with open("models/training_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n📋 Training summary saved.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  🌿 AgriDoc — Model Training (Target: 97%+)")
    print("=" * 60)
    print(f"  Model    : EfficientNetB3")
    print(f"  Dataset  : {DATASET_PATH}")
    print(f"  Strategy : 3-Phase Training + TTA")
    print(f"  Target   : 97%+ Validation Accuracy")

    if not os.path.exists(DATASET_PATH):
        print(f"\n❌ Dataset not found: {DATASET_PATH}")
        return

    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # GPU setup
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        tf.config.experimental.set_memory_growth(gpus[0], True)
        print(f"\n⚡ GPU ready: {gpus[0].name}")
    else:
        print("\n💻 No GPU found, using CPU")

    # Load data
    print("\n📂 Loading dataset...")
    train_gen, val_gen = get_generators()
    num_classes = len(train_gen.class_indices)

    print(f"\n✅ Dataset loaded:")
    print(f"   Classes           : {num_classes}")
    print(f"   Training images   : {train_gen.samples}")
    print(f"   Validation images : {val_gen.samples}")

    if num_classes < 10:
        print("\n❌ ERROR: Less than 10 classes found!")
        print("   Check: data/plantvillage/color/")
        return

    save_class_names(train_gen)

    # Class weights
    print("\n⚖️  Computing class weights...")
    class_weights = get_class_weights(train_gen)
    print(f"   Range: {min(class_weights.values()):.3f} – {max(class_weights.values()):.3f}")

    # Build model
    print("\n🧠 Building EfficientNetB3 model...")
    model, base_model = build_model(num_classes)
    print(f"   Total parameters  : {model.count_params():,}")
    print(f"   Trainable (Phase1): {sum(p.numpy().size for p in model.trainable_weights):,}")

    # ── 3 PHASE TRAINING ──
    phase1_train(model, train_gen, val_gen, class_weights)
    phase2_train(model, base_model, train_gen, val_gen, class_weights)
    phase3_train(model, base_model, train_gen, val_gen, class_weights)

    # Load best weights
    if os.path.exists(WEIGHTS_PATH):
        print(f"\n✅ Loading best weights from {WEIGHTS_PATH}")
        model.load_weights(WEIGHTS_PATH)

    # Save full model
    print(f"\n💾 Saving full model...")
    model.save(MODEL_SAVE_PATH)
    print(f"✅ Model saved to {MODEL_SAVE_PATH}")

    # Final evaluation
    print("\n📊 Final Evaluation:")
    val_loss, val_acc, top5_acc = model.evaluate(val_gen, verbose=1)
    print(f"\n   ✅ Val Accuracy (Top-1) : {val_acc * 100:.2f}%")
    print(f"   ✅ Val Accuracy (Top-5) : {top5_acc * 100:.2f}%")
    print(f"   ✅ Val Loss             : {val_loss:.4f}")

    # TTA
    tta_acc = evaluate_with_tta(model, n_augments=5)
    save_training_summary(val_acc, tta_acc, num_classes)

    print("\n" + "="*60)
    print(f"  🎉 TRAINING COMPLETE!")
    print(f"  🎯 Final Accuracy : {val_acc * 100:.2f}%")
    print(f"  🎯 TTA Accuracy   : {tta_acc * 100:.2f}%")
    print(f"\n  Now run: streamlit run app.py")
    print("="*60)


if __name__ == "__main__":
    main()