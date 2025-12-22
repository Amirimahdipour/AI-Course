<img width="663" height="127" alt="Result 1" src="https://github.com/user-attachments/assets/2899d5d4-f164-40e1-87c2-c222ffad8a09" />﻿# Group 29

Group Members : 
* Armita Partovi 
* Danial Shirdel

# 🐱🐶 Cat vs Dog AI Project

Welcome to the **Cat vs Dog Image Classifier**, powered by **TensorFlow/Keras** — a minimal, CPU-friendly deep learning project that will teach your computer to distinguish cats from dogs.

This project is designed to be **fully runnable on any normal laptop**, even without a GPU, and focuses on **clarity, simplicity, and educational value**.

---

## ⚡ Quick Overview

- **Goal:** Train a small Convolutional Neural Network (CNN) to classify images as **Cat** or **Dog**.
- **Dataset:** TensorFlow built-in `cats_vs_dogs` dataset (automatically downloaded, no manual work).
- **Model:** Sequential CNN with Conv2D, MaxPooling, BatchNormalization, Dropout, and Dense layers.
- **Training:** Uses `binary_crossentropy` loss, `adam` optimizer, and `EarlyStopping` to avoid overfitting.
- **Evaluation:** Prints **accuracy**, **confusion matrix**, and a **classification report** for complete understanding.
- **Prediction:** Can predict on **any local image** and outputs **label + confidence**.

---

## 🛠️ Step-by-Step Instructions

Follow these instructions carefully — **copy-paste only**, and you’re golden.

### 1️⃣ Create a Virtual Environment

This ensures that **all dependencies are isolated** and won’t mess with other Python projects.

```bash
# Use Python 3.11 (TensorFlow does not support 3.14 yet!)
python -m venv venv

Activate before running any scripts so that Python uses the correct dependencies.

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

🧠 You should see (venv) at the start of your terminal prompt — this confirms you’re inside the virtual environment.

Install the exact packages needed for this project. No extras, no missing modules.

pip install tensorflow tensorflow-datasets scikit-learn pillow


⚡ This installs:

- ##TensorFlow: Deep learning framework for building CNNs

- ##TensorFlow Datasets: Easy access to prebuilt datasets like cats_vs_dogs

- ##Scikit-learn: For evaluation metrics (confusion matrix, classification report)

- ##Pillow: For reading images for predictions


# Now, the magic happens. Run the training script:
```
python train.py
```

What happens here:

- ##Dataset is loaded and split into training, validation, and testing sets.

- ##Images are resized to 64x64 pixels and normalized so the model can learn efficiently.

- ##Data augmentation is applied (flip, slight rotation) to make the model more robust.

- ##The CNN is built and compiled.

- ##Training runs for up to 15 epochs, but EarlyStopping ensures it stops once it’s learned enough.

- ##The trained model is saved as model.h5.

💡 On CPU, training might take a few minutes per epoch depending on your laptop — completely normal.


# Check how well your model learned:
```
python evaluate.py
```

Outputs you’ll see:

- ##Confusion Matrix: Shows how many cats were classified correctly, and how many dogs were misclassified.

- ##Classification Report: Shows precision, recall, and F1-score for each class.

🧠 These metrics tell you exactly how confident and accurate your model is.


# Use your model to classify any image:
```
python predict.py sample.jpg
```

Replace sample.jpg with your image path.


⚠️ Important Notes

- ##Python Version: Must be 3.10 or 3.11. TensorFlow does not work with 3.14 yet.

- ##CPU Only: This project runs entirely on CPU. No GPU required.

- ##Dataset Download: First run may take a few minutes (~800MB) for downloading cats_vs_dogs.

- ##Virtual Environment: Always activate it before running scripts.

- ##Image Requirements: Prediction images must be JPG or PNG and RGB.

now your results should look like this :
- ##
<img width="663" height="127" alt="Result 1" src="https://github.com/user-attachments/assets/1679a9d0-3479-449e-8064-cfb65be7d04b" />
- ##
<img width="552" height="267" alt="result 2" src="https://github.com/user-attachments/assets/842eb879-b9f7-46e7-90fd-47f9c97e114a" />
- ##
<img width="212" height="68" alt="result 3" src="https://github.com/user-attachments/assets/88482be2-325b-4155-8ea0-20063a2aef5e" />

hope you figure using it out with my explnations lads :)
```
at the end , this project is nothing against anything related to the AI world , this is like picking a pillow for a fight middle of the world war 3 , so please just skip this and move on , i dont even work in this field tbh :)
but eventually its okay to try at least sometime i guess ...
# 1437
```
