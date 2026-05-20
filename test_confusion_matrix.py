import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load SavedModel
loaded_model = tf.saved_model.load("models/saved_model")

# Inference function
infer = loaded_model.signatures["serving_default"]

# Load class names
with open("models/class_names.txt") as f:
    class_names = [line.strip() for line in f if line.strip()]

# Validation data generator
val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.15
)

val_gen = val_datagen.flow_from_directory(
    "data/plantvillage/color",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

print("Running predictions...")

pred_classes = []

for images, labels in val_gen:

    outputs = infer(tf.constant(images))

    preds = list(outputs.values())[0].numpy()

    pred = np.argmax(preds, axis=1)

    pred_classes.extend(pred)

    if len(pred_classes) >= val_gen.samples:
        break

pred_classes = np.array(pred_classes[:val_gen.samples])

true_classes = val_gen.classes

# Accuracy
accuracy = np.mean(pred_classes == true_classes)

print(f"\nAccuracy: {accuracy*100:.2f}%")

# Classification Report
print("\nClassification Report:\n")

print(classification_report(
    true_classes,
    pred_classes,
    target_names=class_names
))

# Confusion Matrix
cm = confusion_matrix(true_classes, pred_classes)

# Plot confusion matrix
plt.figure(figsize=(15, 12))

sns.heatmap(
    cm,
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.xticks(rotation=90)
plt.yticks(rotation=0)

plt.tight_layout()

plt.show()