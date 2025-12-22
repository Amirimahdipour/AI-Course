"""
Training script for Cat vs Dog classification using TensorFlow/Keras.
- Loads dataset from TensorFlow Datasets
- Preprocesses images (resize + normalize)
- Adds data augmentation
- Builds a Sequential CNN
- Trains with EarlyStopping
- Saves trained model as 'model.h5'
"""

import tensorflow as tf
import tensorflow_datasets as tfds

# -------------------------------
# 1. Load dataset
# -------------------------------
dataset, info = tfds.load(
    "cats_vs_dogs",
    split="train",
    as_supervised=True,
    with_info=True
)

TOTAL = info.splits["train"].num_examples
train_size = int(0.7 * TOTAL)
val_size = int(0.15 * TOTAL)

train_ds = dataset.take(train_size)
val_ds = dataset.skip(train_size).take(val_size)
test_ds = dataset.skip(train_size + val_size)

# -------------------------------
# 2. Preprocessing
# -------------------------------
IMG_SIZE = 64

def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = image / 255.0  # Normalize pixels to [0,1]
    return image, label

# Data augmentation (train only)
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
])

train_ds = (
    train_ds
    .map(preprocess)
    .map(lambda x, y: (data_augmentation(x), y))
    .shuffle(1000)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

val_ds = val_ds.map(preprocess).batch(32)
test_ds = test_ds.map(preprocess).batch(32)

# -------------------------------
# 3. Model
# -------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# -------------------------------
# 4. Compile model
# -------------------------------
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# -------------------------------
# 5. Train
# -------------------------------
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=15,
    callbacks=[early_stop]
)

# -------------------------------
# 6. Save model
# -------------------------------
model.save("model.h5")
print("Model saved as model.h5")
