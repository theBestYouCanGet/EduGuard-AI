# Notebooks — Pipeline ML EduGuard AI

Ce dossier contient les notebooks Google Colab utilisés pour le développement
du modèle de prédiction du décrochage étudiant.

## Structure attendue

| Notebook                   | Étape           | Description                                       |
| -------------------------- | --------------- | ------------------------------------------------- |
| `01_exploration.ipynb`     | EDA             | Exploration et visualisation des données          |
| `02_preprocessing.ipynb`   | Preprocessing   | Nettoyage, encodage, SMOTE, normalisation         |
| `03_modeling.ipynb`        | Modélisation    | Entraînement et comparaison des modèles           |
| `04_evaluation_shap.ipynb` | Évaluation      | Métriques, courbes ROC, explicabilité SHAP        |

## Comment ajouter les notebooks

1. Téléchargez les notebooks depuis Google Drive (dossier `PFE_Dropout/notebooks/`)
2. Placez-les dans ce dossier `notebooks/`
3. Committez : `git add notebooks/ && git commit -m "Add Colab notebooks"`

## Données d'entrée

- **Dataset UCI** : `Predict Students Dropout and Academic Success` (ID 697)
  - Téléchargement : https://archive.ics.uci.edu/dataset/697
  - 4 424 étudiants × 36 variables
- **Dataset FSBM** : données administratives de la Faculté des Sciences Ben M'Sick
  - 6 009 étudiants × 6 variables (Proof of Concept)

## Reproductibilité

Tous les notebooks utilisent `random_state=42` pour garantir la reproductibilité
des résultats. Les artefacts produits (modèles, scaler, encoder) sont sauvegardés
dans `models/` et `models_fsmb/` et utilisés directement par l'application Streamlit.
