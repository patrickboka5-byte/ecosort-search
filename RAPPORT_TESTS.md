# Rapport de tests — Validation Docker & Pipeline complet

## Contexte
Ce rapport documente les tests de validation effectués sur la branche `feature/webapp-docker`, 
couvrant le pipeline complet : scraping Jumia → classification IA → mapping vers les 5 poubelles.

## Test 1 : Construction et exécution Docker

```bash
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```

Construction réussie (~5 min, principalement l'installation de TensorFlow)
Application accessible sur http://localhost:8501
Interface Streamlit fonctionnelle

## Test 2 : Recherche + Scraping

| Recherche | Résultats trouvés |
|---|---|
| shampoing | 5 produits |
| riziere | 4 produits |
| huile | 5 produits |

Le scraping fonctionne correctement dans l'environnement conteneurisé

## Test 3 : Classification IA — Résultats par produit

| Produit testé | Classe prédite | Confiance | Poubelle affichée | Attendu | Correct ? |
|---|---|---|---|---|---|
| Sac de riz (La Rizière) | paper | 36% | 🔵 BLEUE | 🟡 JAUNE (plastique tissé) | ❌ Non |
| Bouteille huile Dinor 1,5L | plastic | 91% | 🟡 JAUNE | 🟡 JAUNE | ✅ Oui |

## Observations

1. **Sur des objets isolés et typiques** (bouteille plastique nette), le modèle est 
   très confiant (91%) et correct.
2. **Sur des emballages atypiques ou complexes** (sac de riz avec motifs et texte), 
   le modèle est peu confiant (36%) et se trompe.
3. Cette limite est probablement liée à la nature du dataset Kaggle utilisé pour 
   l'entraînement, qui contient des objets isolés simples plutôt que des emballages 
   commerciaux réels avec impressions complexes.

## Recommandations

- Afficher un avertissement visuel quand la confiance est en dessous d'un seuil 
  (ex: 60%), du type "Prédiction incertaine, vérifiez visuellement"
- Envisager d'enrichir le dataset d'entraînement avec des exemples d'emballages 
  commerciaux réels si le temps le permet
- Documenter cette limite connue dans le README principal du projet