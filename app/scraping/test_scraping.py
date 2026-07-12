from scraper import chercher_produits_jumia

if __name__ == "__main__":
    while True:
        mot_cle = input("\nEntrez un produit à rechercher (ou 'quit' pour arrêter) : ")
        if mot_cle.lower() == "quit":
            print("Fin des tests.")
            break
        produits = chercher_produits_jumia(mot_cle)
        for p in produits:
            print(p)
        print(f"\n→ {len(produits)} produit(s) trouvé(s) pour '{mot_cle}'")