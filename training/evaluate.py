import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

# ---------- 1. Parametres (identiques a train.py) ----------
DATA_DIR = "dataset/Garbage classification/Garbage classification"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# ---------- 2. On recharge le meme jeu de validation ----------
# Meme seed + meme split = exactement les memes images
# que celles jamais vues pendant l'entrainement
val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,   # important : garder l'ordre pour comparer
)
class_names = val_ds.class_names
print("Classes :", class_names)

# ---------- 3. Chargement du modele entraine ----------
model = keras.models.load_model("models/modele_eco_sort.h5")

# ---------- 4. Predictions sur toute la validation ----------
y_true = []
y_pred = []
for images, labels in val_ds:
    preds = model.predict(images, verbose=0)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(preds, axis=1))
y_true = np.array(y_true)
y_pred = np.array(y_pred)
# ---------- 5. Rapport detaille par classe ----------
print(classification_report(y_true, y_pred, target_names=class_names))

# ---------- 6. Matrice de confusion en image ----------
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
fig, ax = plt.subplots(figsize=(8, 8))
disp.plot(ax=ax, cmap="Blues", xticks_rotation=45)
plt.title("Matrice de confusion - EcoSort")
plt.tight_layout()
plt.savefig("training/matrice_confusion.png")
print("Matrice sauvegardee dans training/matrice_confusion.png")