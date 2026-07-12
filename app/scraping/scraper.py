import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def chercher_produits_jumia(mot_cle: str, nb_resultats: int = 5) -> list[dict]:
    """
    Recherche des produits sur Jumia CI à partir d'un mot-clé.
    Retourne une liste de dictionnaires : nom, prix, image, lien.
    Retourne une liste vide en cas d'erreur ou d'absence de résultats.
    """
    mot_cle_encode = quote(mot_cle)  # gère les espaces et caractères spéciaux
    url = f"https://www.jumia.ci/catalog/?q={mot_cle_encode}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"Erreur : la requête vers Jumia a dépassé le délai d'attente.")
        return []
    except requests.exceptions.ConnectionError:
        print(f"Erreur : impossible de se connecter à Jumia (vérifiez votre connexion internet).")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP : {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Erreur inattendue lors de la requête : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="prd")

    if not articles:
        print(f"Aucun résultat trouvé pour '{mot_cle}'.")
        return []

    resultats = []
    for article in articles:
        if len(resultats) >= nb_resultats:
            break

        lien_tag = article.find("a", class_="core")
        nom_tag = article.find("h3", class_="name")
        prix_tag = article.find("div", class_="prc")
        img_tag = article.find("img")

        if not (lien_tag and nom_tag):
            continue  # bloc incomplet (souvent une publicité), on l'ignore

        produit = {
            "nom": nom_tag.get_text(strip=True),
            "prix": prix_tag.get_text(strip=True) if prix_tag else None,
            "image_url": img_tag.get("data-src") if img_tag else None,
            "lien": "https://www.jumia.ci" + lien_tag.get("href", "")
        }
        resultats.append(produit)

    return resultats

