"""Tests du module mapping : on verifie les 3 chemins de decision."""
from mapping import determiner_poubelle, est_electronique

# Chaque cas : (titre produit, classe predite par le modele, poubelle attendue)
CAS_DE_TEST = [
    # --- Regle D3E prioritaire (le modele ne doit pas etre ecoute) ---
    ("Chargeur USB-C rapide 25W Samsung", "plastic", "D3E"),
    ("Ecouteurs Bluetooth sans fil",      "plastic", "D3E"),
    ("Smartphone Tecno Spark 20",         "metal",   "D3E"),
    ("Blender mixeur 2L 350W",            "plastic", "D3E"),
    # --- Regle 2 : le modele decide ---
    ("Bouteille de jus de bissap 1L",     "glass",   "VERTE"),
    ("Pack de 6 bouteilles d'eau Awa",    "plastic", "JAUNE"),
    ("Boite de conserve tomates 400g",    "metal",   "JAUNE"),
    ("Carton de demenagement 60x40",      "cardboard", "JAUNE"),
    ("Cahier 200 pages grand format",     "paper",   "BLEUE"),
    ("Sachet plastique alimentaire x100", "trash",   "MARRON"),
    # --- Securite : classe inconnue ---
    ("Produit mysterieux",                None,      "MARRON"),
]

reussis = 0
for titre, classe, attendu in CAS_DE_TEST:
    resultat = determiner_poubelle(titre, classe)
    ok = resultat["code"] == attendu
    reussis += ok
    statut = "OK  " if ok else "FAIL"
    print(f"[{statut}] {titre[:40]:40} classe={str(classe):10} -> {resultat['code']:6} (attendu {attendu})")

print(f"\n{reussis}/{len(CAS_DE_TEST)} tests reussis")