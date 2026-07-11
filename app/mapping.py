"""Traduction des classes du modele vers les 5 poubelles officielles.

Regle 1 (prioritaire) : detection D3E par mots-cles dans le titre du produit.
Regle 2 : mapping classe du modele -> poubelle.
"""

# ---------- Les 5 poubelles officielles du sujet ----------
POUBELLES = {
    "JAUNE":  {"nom": "Poubelle JAUNE",        "couleur": "#F1C40F", "description": "Emballages menagers legers : plastique, metal, carton"},
    "VERTE":  {"nom": "Poubelle VERTE",        "couleur": "#27AE60", "description": "Verre d'emballage : bouteilles, pots, bocaux"},
    "BLEUE":  {"nom": "Poubelle BLEUE",        "couleur": "#2980B9", "description": "Papiers graphiques propres : journaux, cahiers, livres"},
    "D3E":    {"nom": "Bac Electronique (D3E)", "couleur": "#7F8C8D", "description": "Produits a piles, batterie ou prise electrique"},
    "MARRON": {"nom": "Poubelle MARRON/NOIRE", "couleur": "#6E4B3A", "description": "Dechets residuels non recyclables"},
}

# ---------- Regle 2 : classe du modele -> poubelle ----------
CLASSE_VERS_POUBELLE = {
    "plastic":   "JAUNE",
    "metal":     "JAUNE",
    "cardboard": "JAUNE",
    "glass":     "VERTE",
    "paper":     "BLEUE",
    "trash":     "MARRON",
}

# ---------- Regle 1 : mots-cles D3E (prioritaire) ----------
MOTS_CLES_D3E = [
    "telephone", "smartphone", "phone", "iphone", "samsung galaxy",
    "ecouteur", "casque", "earbuds", "airpods", "headphone",
    "chargeur", "charger", "cable usb", "usb", "adaptateur", "power bank",
    "batterie", "battery", "pile",
    "montre connectee", "smartwatch", "montre digitale",
    "mixeur", "blender", "ventilateur", "fer a repasser", "bouilloire",
    "ordinateur", "laptop", "tablette", "tablet", "television", "tv led",
    "radio", "enceinte", "speaker", "souris", "clavier", "console",
    "ampoule", "lampe led", "rasoir electrique", "tondeuse",
]


def _normaliser(texte: str) -> str:
    """Minuscules + suppression des accents courants pour comparer sereinement."""
    texte = texte.lower()
    for avant, apres in [("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"), ("î", "i"), ("ô", "o"), ("û", "u"), ("ç", "c")]:
        texte = texte.replace(avant, apres)
    return texte


def est_electronique(titre_produit: str) -> bool:
    """Regle 1 : le titre contient-il un mot-cle D3E ?"""
    titre = _normaliser(titre_produit)
    return any(mot in titre for mot in MOTS_CLES_D3E)


def determiner_poubelle(titre_produit: str, classe_modele: str = None) -> dict:
    """Point d'entree principal : renvoie la poubelle sous forme de dict
    {code, nom, couleur, description}.

    - titre_produit : le titre scrape sur Jumia
    - classe_modele : la classe predite par le CNN (peut etre None si
      la regle D3E suffit)
    """
    if est_electronique(titre_produit):
        code = "D3E"
    elif classe_modele in CLASSE_VERS_POUBELLE:
        code = CLASSE_VERS_POUBELLE[classe_modele]
    else:
        code = "MARRON"  # securite : en cas de doute, dechet residuel

    resultat = dict(POUBELLES[code])
    resultat["code"] = code
    return resultat