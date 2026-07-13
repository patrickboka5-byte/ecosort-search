import streamlit as st

st.set_page_config(page_title="EcoSort-Search", layout="centered")

PRODUITS_FACTICES = [
    {"titre": "Chargeur USB-C rapide 25W", "prix": "3 500 FCFA",
     "image_url": "https://placehold.co/300x300?text=Chargeur", "lien": "#"},
    {"titre": "Bouteille en verre 1L", "prix": "1 200 FCFA",
     "image_url": "https://placehold.co/300x300?text=Bouteille", "lien": "#"},
    {"titre": "Cahier 200 pages grand format", "prix": "800 FCFA",
     "image_url": "https://placehold.co/300x300?text=Cahier", "lien": "#"},
    {"titre": "Pack 6 bouteilles d'eau minerale", "prix": "2 000 FCFA",
     "image_url": "https://placehold.co/300x300?text=Eau", "lien": "#"},
]

def rechercher(mot_cle):
    mot = mot_cle.lower()
    resultats = [p for p in PRODUITS_FACTICES if mot in p["titre"].lower()]
    return resultats if resultats else PRODUITS_FACTICES

st.title("EcoSort-Search")
st.subheader("Trouvez la bonne poubelle pour chaque produit")

mot_cle = st.text_input("Entrez le nom d'un produit :")

if mot_cle:
    produits = rechercher(mot_cle)
    st.write(str(len(produits)) + " produit(s) trouve(s) :")

    for i, produit in enumerate(produits):
        col_image, col_infos = st.columns([1, 2])
        with col_image:
            st.image(produit["image_url"], width=150)
        with col_infos:
            st.markdown("**" + produit["titre"] + "**")
            st.write(produit["prix"])
            if st.button("Ou jeter ce produit ?", key="btn_" + str(i)):
                st.session_state["produit_choisi"] = produit

    if "produit_choisi" in st.session_state:
        choisi = st.session_state["produit_choisi"]
        st.divider()
        st.success("Produit selectionne : " + choisi["titre"])
