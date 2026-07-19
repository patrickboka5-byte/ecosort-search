import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from mapping import determiner_poubelle, est_electronique
from classifier import classifier_image_url
from scraping.scraper import chercher_produits_jumia

st.set_page_config(page_title="EcoSort-Search", layout="centered", page_icon="♻️")

# ---------------------------------------------------------------------------
# STYLE GLOBAL
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #F7F8F7; }
    .block-container { padding-top: 0rem; max-width: 900px; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes popIn {
        0%   { opacity: 0; transform: scale(0.85); }
        70%  { opacity: 1; transform: scale(1.03); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* --- Hero plein cadre, style institutionnel --- */
    .hero-banner {
        position: relative;
        width: 100%;
        min-height: 480px;
        border-radius: 0 0 28px 28px;
        background-image:
            linear-gradient(180deg, rgba(8,20,14,0.25) 0%, rgba(8,20,14,0.15) 40%, rgba(6,16,11,0.85) 100%),
            url("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center 30%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 3rem 2.4rem 4.5rem 2.4rem;
        margin-bottom: 0;
    }
    .hero-eyebrow {
        color: #9BE8B8;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .hero-banner h1 {
        color: white;
        font-size: 2.7rem;
        font-weight: 800;
        line-height: 1.08;
        margin: 0 0 0.7rem 0;
        letter-spacing: -0.5px;
        max-width: 640px;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.88);
        font-size: 1.08rem;
        max-width: 520px;
        margin: 0;
    }

    /* --- Barre de recherche flottante, chevauche le bas du hero --- */
    div[data-testid="stTextInput"] {
        margin-top: -34px;
        position: relative;
        z-index: 6;
        padding: 0 1.6rem;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18) !important;
        padding: 1.1rem 1.3rem !important;
        font-size: 1.02rem !important;
        background: white !important;
    }
    div[data-testid="stTextInput"] label { display: none; }

    .trust-line {
        text-align: center;
        color: #5B6B62;
        font-size: 0.92rem;
        margin: 1.6rem 0 0.4rem 0;
        animation: fadeInUp 0.5s ease-out;
    }

    /* --- Cartes produits --- */
    .product-card {
        background: white;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #ECEFED;
        animation: fadeInUp 0.45s ease-out both;
    }
    .product-title { font-weight: 700; font-size: 1.02rem; color: #16281F; margin-bottom: 0.15rem; }
    .product-price { color: #2E7D4F; font-weight: 600; margin-bottom: 0.5rem; }

    .source-badge {
        display: inline-block;
        background: #E7F3EC;
        color: #1E6B3E;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 1.8rem 0 1.2rem 0;
        animation: fadeInUp 0.4s ease-out;
    }

    /* --- Verdict final --- */
    .verdict-box {
        padding: 20px 28px 30px 28px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 28px rgba(0,0,0,0.16);
        margin-top: 0.5rem;
        animation: popIn 0.45s ease-out both;
    }
    .verdict-icon {
        font-size: 3.4rem;
        line-height: 1;
        margin-bottom: 6px;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.25));
    }
    .verdict-box h2 { color: white; margin: 0; font-size: 1.7rem; font-weight: 800; }
    .verdict-box p { color: rgba(255,255,255,0.95); margin: 10px 0 0 0; font-size: 1.02rem; }

    .stButton>button {
        border-radius: 10px;
        border: 1.5px solid #2E7D4F;
        color: #2E7D4F;
        font-weight: 600;
        padding: 0.4rem 1rem;
        background: white;
        transition: all 0.15s ease;
    }
    .stButton>button:hover { background: #2E7D4F; color: white; border-color: #2E7D4F; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HERO PLEIN CADRE
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-eyebrow">Tri selectif intelligent</div>
    <h1>Trouvez la bonne poubelle pour chaque produit</h1>
    <p>Recherchez un produit, notre intelligence artificielle analyse son emballage
    et vous indique instantanement la consigne de tri a suivre.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# BARRE DE RECHERCHE (flotte sur le bord bas du hero via CSS)
# ---------------------------------------------------------------------------
mot_cle = st.text_input(
    "Recherche",
    placeholder="Rechercher un produit : shampoing, cahier, chargeur telephone...",
    key="search_input",
    label_visibility="collapsed",
)

PRODUITS_FACTICES = [
    {"titre": "Chargeur USB-C rapide 25W (demo)", "prix": "3 500 FCFA",
     "image_url": "https://placehold.co/300x300.png?text=Chargeur", "lien": "#"},
    {"titre": "Bouteille en verre 1L (demo)", "prix": "1 200 FCFA",
     "image_url": "https://placehold.co/300x300.png?text=Bouteille", "lien": "#"},
]

BIN_VISUALS = [
    ("JAUNE",  "🟡", "#F1C40F"),
    ("VERT",   "🟢", "#27AE60"),
    ("BLEU",   "🔵", "#2E86C1"),
    ("D3E",    "🔌", "#7F8C8D"),
    ("GRIS",   "🔌", "#7F8C8D"),
    ("MARRON", "🟤", "#6E4A2E"),
    ("NOIRE",  "⚫", "#2C2C2C"),
]

def icone_pour_poubelle(nom_poubelle):
    nom_maj = nom_poubelle.upper()
    for cle, emoji, _ in BIN_VISUALS:
        if cle in nom_maj:
            return emoji
    return "♻️"

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

    icone = icone_pour_poubelle(poubelle["nom"])

    st.markdown(
        "<div class='verdict-box' style='background-color:" + poubelle["couleur"] + ";'>"
        "<div class='verdict-icon'>" + icone + "</div>"
        "<h2>" + poubelle["nom"] + "</h2>"
        "<p>" + poubelle["description"] + "</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption(explication)

    if any(mot in poubelle["nom"].upper() for mot in ["JAUNE", "VERT", "BLEU"]):
        st.balloons()

# ---------------------------------------------------------------------------
# ETAT "AVANT RECHERCHE" : simple ligne de confiance, sans emoji
# ---------------------------------------------------------------------------
if not mot_cle:
    st.markdown(
        "<p class='trust-line'>Recherche en direct parmi les produits Jumia — "
        "classification automatique selon les 5 categories officielles de tri.</p>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# RECHERCHE
# ---------------------------------------------------------------------------
if mot_cle:
    with st.spinner("Recherche sur Jumia..."):
        produits, source = rechercher(mot_cle)

    st.markdown(
        "<span class='source-badge'>" + str(len(produits)) + " produit(s) trouve(s) — source : " + source + "</span>",
        unsafe_allow_html=True,
    )

    for i, produit in enumerate(produits):
        with st.container():
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            col_image, col_infos = st.columns([1, 2])
            with col_image:
                if produit["image_url"]:
                    st.image(produit["image_url"], width=140)
            with col_infos:
                st.markdown("<div class='product-title'>" + produit["titre"] + "</div>", unsafe_allow_html=True)
                st.markdown("<div class='product-price'>" + produit["prix"] + "</div>", unsafe_allow_html=True)
                if st.button("Où jeter ce produit ?", key="btn_" + str(i)):
                    st.session_state["produit_choisi"] = produit
            st.markdown("</div>", unsafe_allow_html=True)

    if "produit_choisi" in st.session_state:
        st.divider()
        afficher_verdict(st.session_state["produit_choisi"])