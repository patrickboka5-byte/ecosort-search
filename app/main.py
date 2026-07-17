import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from mapping import determiner_poubelle, est_electronique
from classifier import classifier_image_url
from scraping.scraper import chercher_produits_jumia

st.set_page_config(page_title="EcoSort-Search", layout="centered")

PRODUITS_FACTICES = [
    {"titre": "Chargeur USB-C rapide 25W (demo)", "prix": "3 500 FCFA",
     "image_url": "https://placehold.co/300x300.png?text=Chargeur", "lien": "#"},
    {"titre": "Bouteille en verre 1L (demo)", "prix": "1 200 FCFA",
     "image_url": "https://placehold.co/300x300.png?text=Bouteille", "lien": "#"},
]

def adapter_produit(p):
    """Normalise un produit du scraper vers le vocabulaire officiel de l'app.
    Tolere 'nom' (version actuelle du scraper) et 'titre' (contrat officiel)."""
    return {
        "titre": p.get("titre") or p.get("nom") or "Produit sans titre",
        "prix": p.get("prix") or "Prix indisponible",
        "image_url": p.get("image_url"),
        "lien": p.get("lien") or "#",
    }

def rechercher(mot_cle):
    """Vrai scraping Jumia ; produits factices en secours si echec."""
    try:
        produits = chercher_produits_jumia(mot_cle)
    except Exception:
        produits = []
    if produits:
        return [adapter_produit(p) for p in produits], "Jumia"
    return PRODUITS_FACTICES, "demo (Jumia inaccessible)"

def afficher_verdict(produit):
    titre = produit["titre"]
    if est_electronique(titre):
        poubelle = determiner_poubelle(titre)
        explication = "Detecte comme appareil electronique (mots-cles)"
    elif not produit["image_url"]:
        poubelle = determiner_poubelle(titre, None)
        explication = "Pas d'image disponible, classement par defaut"
    else:
        try:
            with st.spinner("Analyse de l'image par l'IA..."):
                classe, confiance = classifier_image_url(produit["image_url"])
            poubelle = determiner_poubelle(titre, classe)
            explication = "Matiere predite : " + classe + " (" + str(round(confiance * 100)) + "% de confiance)"
        except Exception:
            poubelle = determiner_poubelle(titre, None)
            explication = "Image inaccessible, classement par defaut"
    st.markdown(
        "<div style='background-color:" + poubelle["couleur"] + ";"
        "padding:30px;border-radius:12px;text-align:center;'>"
        "<h2 style='color:white;margin:0;'>" + poubelle["nom"] + "</h2>"
        "<p style='color:white;margin:8px 0 0 0;'>" + poubelle["description"] + "</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption(explication)

st.title("EcoSort-Search")
st.subheader("Trouvez la bonne poubelle pour chaque produit")

mot_cle = st.text_input("Entrez le nom d'un produit :")

if mot_cle:
    with st.spinner("Recherche sur Jumia..."):
        produits, source = rechercher(mot_cle)
    st.write(str(len(produits)) + " produit(s) trouve(s) — source : " + source)
    for i, produit in enumerate(produits):
        col_image, col_infos = st.columns([1, 2])
        with col_image:
            if produit["image_url"]:
                st.image(produit["image_url"], width=150)
        with col_infos:
            st.markdown("**" + produit["titre"] + "**")
            st.write(produit["prix"])
            if st.button("Ou jeter ce produit ?", key="btn_" + str(i)):
                st.session_state["produit_choisi"] = produit
    if "produit_choisi" in st.session_state:
        st.divider()
        afficher_verdict(st.session_state["produit_choisi"])
