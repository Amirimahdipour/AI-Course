"""
Evaluation script for Cat vs Dog model.
- Loads trained model
- Evaluates on full dataset
- Prints accuracy, confusion matrix, classification report
"""

import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Load model
model = tf.keras.models.load_model("model.h5")

# Load dataset
dataset = tfds.load("cats_vs_dogs", split="train", as_supervised=True)

IMG_SIZE = 64

def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = image / 255.0
    return image, label

dataset = dataset.map(preprocess).batch(32)

# Collect predictions and true labels
y_true = []
y_pred = []

for images, labels in dataset:
    preds = model.predict(images, verbose=0)
    preds = (preds > 0.5).astype(int)

    y_true.extend(labels.numpy())
    y_pred.extend(preds.flatten())

# Metrics
print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=["Cat", "Dog"]))
