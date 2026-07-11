import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# ---------- 1. Parametres ----------
DATA_DIR = "dataset/Garbage classification/Garbage classification"
IMG_SIZE = (224, 224)   # taille attendue par MobileNetV2
BATCH_SIZE = 32
EPOCHS = 10
SEED = 42

# ---------- 2. Chargement des donnees ----------
# 80% des images pour apprendre, 20% pour valider
train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
)
val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
)

class_names = train_ds.class_names
print("Classes detectees :", class_names)

# Optimisation de la lecture des images
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ---------- 3. Augmentation des donnees ----------
# On cree des variantes des images (miroir, rotation, zoom)
# pour que le modele generalise mieux
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# ---------- 4. Le modele : MobileNetV2 + notre tete ----------
base_model = keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False,       # on retire sa couche finale d'origine
    weights="imagenet",      # on garde son savoir pre-entraine
)
base_model.trainable = False  # on GELE son savoir

inputs = keras.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = layers.Rescaling(1./127.5, offset=-1)(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(len(class_names), activation="softmax")(x)
model = keras.Model(inputs, outputs)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.summary()

# ---------- 5. Entrainement ----------
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# ---------- 6. Sauvegarde ----------
model.save("models/modele_eco_sort.h5")
model.save("models/modele_eco_sort.keras")
print("Modele sauvegarde dans models/modele_eco_sort.h5")

# ---------- 7. Courbes d'apprentissage ----------
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="train")
plt.plot(history.history["val_accuracy"], label="validation")
plt.title("Precision")
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="train")
plt.plot(history.history["val_loss"], label="validation")
plt.title("Perte")
plt.legend()
plt.savefig("training/courbes_apprentissage.png")
print("Courbes sauvegardees dans training/courbes_apprentissage.png")