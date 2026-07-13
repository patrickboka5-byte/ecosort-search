"""Chargement du modele et classification d'une image produit."""
import numpy as np
from io import BytesIO
import requests
from PIL import Image
from tensorflow import keras

CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
IMG_SIZE = (224, 224)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

_modele = None  # charge une seule fois, puis reutilise

def charger_modele():
    global _modele
    if _modele is None:
        _modele = keras.models.load_model("models/modele_eco_sort.h5")
    return _modele

def classifier_image(image):
    """Classifie un objet PIL.Image deja ouvert. Renvoie (classe, confiance)."""
    image = image.convert("RGB").resize(IMG_SIZE)
    tableau = np.expand_dims(np.array(image), axis=0)
    predictions = charger_modele().predict(tableau, verbose=0)[0]
    indice = int(np.argmax(predictions))
    return CLASSES[indice], float(predictions[indice])

def classifier_image_url(image_url):
    """Telecharge une image par son URL puis la classifie."""
    reponse = requests.get(image_url, headers=HEADERS, timeout=15)
    reponse.raise_for_status()
    return classifier_image(Image.open(BytesIO(reponse.content)))

if __name__ == "__main__":
    # Test 1 : image locale du dataset si disponible, sinon image generee
    import os, glob
    candidats = glob.glob("dataset/**/glass/*.jpg", recursive=True)
    if candidats:
        print("Test avec une image du dataset :", candidats[0])
        classe, confiance = classifier_image(Image.open(candidats[0]))
    else:
        print("Pas de dataset local : test avec une image unie (verifie juste la mecanique)")
        classe, confiance = classifier_image(Image.new("RGB", (300, 300), (0, 120, 60)))
    print("Classe predite :", classe, "| confiance :", round(confiance * 100, 1), "%")
