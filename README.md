# 🎓 EduGuard AI — Système Intelligent et Explicable de Prédiction Précoce du Décrochage Étudiant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-FF4B4B.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-orange.svg)
![SHAP](https://img.shields.io/badge/SHAP-0.43+-9C27B0.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-PFE%202026-success.svg)

**Projet de Fin d'Études — Licence d'Excellence en Intelligence Artificielle**

**Faculté des Sciences Ben M'Sick — Université Hassan II Casablanca**

</div>

---

## 📋 Table des matières

- [Contexte](#-contexte)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Résultats](#-résultats)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Dataset](#-dataset)
- [Adaptation au contexte marocain](#-adaptation-au-contexte-marocain)
- [Auteurs](#-auteurs)
- [Licence](#-licence)

---

## 🎯 Contexte

Le décrochage étudiant constitue un défi majeur pour les établissements d'enseignement supérieur. Les méthodes traditionnelles de suivi pédagogique, **réactives par nature**, interviennent souvent trop tard pour permettre une prise en charge efficace des étudiants en difficulté.

**EduGuard AI** est un système intelligent de détection précoce du risque de décrochage étudiant, basé sur des techniques de Machine Learning. Il combine :

- ⚡ **Performance prédictive** — modèle XGBoost atteignant 76 % d'accuracy et 0.914 d'AUC sur la classe Dropout
- 🔍 **Explicabilité** — intégration native de SHAP pour justifier chaque prédiction
- 🖥️ **Interface opérationnelle** — application web Streamlit destinée aux responsables pédagogiques
- 🇲🇦 **Adaptation locale** — Proof of Concept sur données réelles de la FSBM

## ✨ Fonctionnalités

### Application web EduGuard AI

- 🔐 **Page de connexion sécurisée** — authentification par responsable de filière
- 🏠 **Tableau de bord** — vue d'ensemble et navigation
- 👤 **Prédiction individuelle** — saisie manuelle des 36 variables d'un étudiant
  - Affichage de la classe prédite (Abandon / Inscrit / Diplômé)
  - Affichage des probabilités par classe
  - Niveau de risque (Critique / Élevé / Moyen / Faible)
  - **Graphique SHAP** — top 15 facteurs explicatifs de la prédiction
- 📊 **Prédiction en batch** — upload d'un fichier CSV contenant plusieurs étudiants
  - Validation automatique du format
  - Téléchargement des résultats avec prédictions et probabilités
- 🇲🇦 **Adaptation FSBM** — Proof of Concept sur données marocaines (6 variables)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Streamlit                    │
│  ┌──────────┐  ┌────────────┐  ┌────────┐  ┌────────────┐  │
│  │  Login   │→ │  Accueil   │→ │ Pred.  │→ │   Batch    │  │
│  │ (YAML)   │  │  (Stats)   │  │ Indiv. │  │   (CSV)    │  │
│  └──────────┘  └────────────┘  └────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      utils.py (cœur)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  XGBoost    │  │  Standard   │  │   SHAP Explainer    │  │
│  │  (model)    │  │  Scaler     │  │  (TreeExplainer)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Modèles pré-entraînés                    │
│  models/         →  XGBoost (UCI 36 features)               │
│  models_fsmb/    →  Random Forest (FSBM 6 features, POC)    │
└─────────────────────────────────────────────────────────────┘
```

### Stack technique

| Composant           | Technologie                  |
| ------------------- | ---------------------------- |
| Langage             | Python 3.11+                 |
| Application web     | Streamlit ≥ 1.45             |
| Modèle ML principal | XGBoost ≥ 2.0                |
| Modèle POC FSBM     | scikit-learn Random Forest   |
| Explicabilité       | SHAP ≥ 0.43                  |
| Prétraitement       | scikit-learn, imbalanced-learn (SMOTE) |
| Manipulation données| pandas, NumPy                |
| Visualisation       | matplotlib                   |
| Configuration       | PyYAML + python-dotenv       |

## 📊 Résultats

### Modèle principal (UCI — 36 variables, 3 classes)

| Modèle                   | Accuracy | F1 Weighted | F1 Dropout |
| ------------------------ | -------- | ----------- | ---------- |
| Régression Logistique    | 73.6 %   | 0.748       | —          |
| Random Forest            | 76.0 %   | 0.762       | —          |
| **XGBoost (modèle final)** | **76.0 %** | **0.757** | **0.763**  |

**Courbes ROC (XGBoost)** :

| Classe    | AUC    | Interprétation                  |
| --------- | ------ | ------------------------------- |
| Graduate  | 0.930  | Excellente capacité discriminante |
| Dropout   | 0.914  | Très bonne capacité discriminante |
| Enrolled  | 0.819  | Bonne capacité discriminante    |

### Proof of Concept FSBM (6 variables, 2 classes)

- **Accuracy** : 84.6 %
- **Modèle** : Random Forest (200 estimateurs, max_depth=10)
- **Features dominantes** : Notes S2 (52.2 %) + Notes S1 (40.3 %) = 92.5 % de l'importance

### Top 5 des facteurs de risque identifiés (EDA)

| Rang | Facteur                 | Type                 | Signal              |
| ---- | ----------------------- | -------------------- | ------------------- |
| 1    | Frais non payés         | Financier dynamique  | 86.6 % Dropout      |
| 2    | Note = 0 en S1 ET S2    | Académique critique  | 80.8 % Dropout      |
| 3    | Absence de bourse       | Financier initial    | 38.7 % vs 12.2 %    |
| 4    | Notes faibles           | Académique progressif| Séparation nette    |
| 5    | Âge élevé               | Démographique        | Médiane 23 vs 20 ans|

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Option 1 — Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/VOTRE-USERNAME/EduGuard-AI.git
cd EduGuard-AI

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Sur Linux/macOS :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos identifiants

# 6. Lancer l'application
streamlit run app/app.py
```

L'application sera accessible sur **http://localhost:8501**

### Option 2 — Avec Docker

```bash
# Construction et lancement en une commande
docker-compose up --build

# Ou sans docker-compose :
docker build -t eduguard-ai .
docker run -p 8501:8501 eduguard-ai
```

L'application sera accessible sur **http://localhost:8501**

## 🖥️ Utilisation

### Comptes de démonstration

Une fois l'application lancée, connectez-vous avec l'un des comptes suivants
(à configurer dans le fichier `.env`) :

| Identifiant            | Département             | Rôle         |
| ---------------------- | ----------------------- | ------------ |
| `chef_informatique`    | Informatique            | Chef filière |
| `chef_gestion`         | Gestion                 | Chef filière |
| `chef_tourisme`        | Tourisme                | Chef filière |
| `chef_infirmiers`      | Soins infirmiers        | Chef filière |
| `chef_ingenierie`      | Ingénierie informatique | Chef filière |
| `admin`                | Administration          | Admin        |

### Workflow type

1. **Connexion** avec votre identifiant de chef de filière
2. **Prédiction individuelle** : saisissez les informations d'un étudiant → obtenez la prédiction + explication SHAP
3. **Prédiction batch** : uploadez un CSV contenant plusieurs étudiants → téléchargez les résultats
4. **Adaptation FSBM** : utilisez le modèle POC marocain (6 variables simplifiées)

### Format CSV pour prédiction batch

Le fichier CSV doit contenir les colonnes suivantes (voir `app/utils.py → ALL_FEATURES`) :

```
Marital Status, Application mode, Application order, Course, ...
1, 1, 1, 9119, ...
2, 17, 5, 9130, ...
```

Un template est téléchargeable directement depuis l'application (page **Prédiction Batch**).

## 📁 Structure du projet

```
EduGuard-AI/
├── app/                          # Application Streamlit
│   ├── app.py                    # Point d'entrée + layout principal
│   ├── utils.py                  # Modèle UCI — chargement, prédiction, SHAP
│   ├── utils_fsmb.py             # Modèle FSBM — utils pour le POC marocain
│   ├── config.yaml               # Configuration utilisateurs (sans mots de passe)
│   ├── requirements.txt          # Dépendances (legacy — voir /requirements.txt à la racine)
│   ├── logo_fsbm.png             # Logo FSBM
│   └── pages/                    # Pages de l'application
│       ├── accueil.py            # Tableau de bord
│       ├── login.py              # Authentification
│       ├── prediction.py         # Prédiction individuelle (UCI)
│       ├── batch.py              # Prédiction batch (CSV)
│       └── prediction_fsmb.py    # Prédiction POC FSBM
│
├── models/                       # Modèle principal UCI (36 features, 3 classes)
│   ├── model.json                # XGBoost — format natif (recommandé)
│   ├── model.pkl                 # XGBoost — pickle (fallback)
│   ├── scaler.pkl                # StandardScaler
│   ├── scaler.joblib             # StandardScaler (joblib)
│   ├── encoder.pkl               # LabelEncoder
│   ├── encoder.joblib            # LabelEncoder (joblib)
│   ├── shap_explainer.pkl        # SHAP TreeExplainer
│   └── shap_explainer_v2.pkl     # SHAP TreeExplainer (v2)
│
├── models_fsmb/                  # Modèle POC FSBM (6 features, 2 classes)
│   ├── model_fsmb.pkl            # Random Forest
│   ├── scaler_fsmb.pkl           # StandardScaler FSBM
│   ├── encoders_fsmb.pkl         # Encodeurs FSBM
│   └── shap_explainer_fsmb.pkl   # SHAP explainer FSBM
│
├── notebooks/                    # Notebooks Colab (à ajouter)
│   └── README.md                 # Instructions pour ajouter les notebooks
│
├── data/                         # Données brutes (gitignored)
│   └── .gitkeep
│
├── docs/                         # Documentation complémentaire
│   └── README.md
│
├── .env.example                  # Template des variables d'environnement
├── .gitignore                    # Fichiers ignorés par Git
├── Dockerfile                    # Image Docker
├── docker-compose.yml            # Orchestration Docker
├── LICENSE                       Licence MIT
├── PUSH_TO_GITHUB.md             # Guide pas-à-pas pour publier sur GitHub
├── README.md                     # Ce fichier
└── requirements.txt              # Dépendances Python (racine)
```

## 📦 Dataset

### Dataset principal — UCI Machine Learning Repository

- **Nom** : *Predict Students Dropout and Academic Success*
- **Identifiant UCI** : 697
- **Source** : Établissement d'enseignement supérieur portugais (cohorte 2008–2019)
- **Taille** : 4 424 étudiants × 36 variables
- **Cible** : 3 classes (Dropout / Enrolled / Graduate)
- **Téléchargement** : https://archive.ics.uci.edu/dataset/697

### Citation

```
Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021).
Predict Students' Dropout and Academic Success.
UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.
```

## 🇲🇦 Adaptation au contexte marocain

En plus du modèle principal entraîné sur le dataset UCI portugais, ce projet inclut un **Proof of Concept** adapté au contexte marocain, entraîné sur des données réelles de la **Faculté des Sciences Ben M'Sick (FSBM)**.

| Caractéristique       | Modèle UCI           | Modèle FSBM (POC)         |
| --------------------- | -------------------- | ------------------------- |
| Source des données    | Portugal (UCI)       | FSBM (Maroc)              |
| Nombre d'étudiants    | 4 424                | 6 009                     |
| Nombre de variables   | 36                   | 6                         |
| Classes               | 3 (Dropout/Enrolled/Graduate) | 2 (Abandon/Réinscription) |
| Algorithme            | XGBoost              | Random Forest             |
| Accuracy              | 76.0 %               | 84.6 %                    |
| AUC Dropout           | 0.914                | —                         |

**Variables FSBM** : Notes S1, Notes S2, Type de baccalauréat, Filière, Genre, Année d'inscription.

> ⚠️ Le modèle FSBM est un **Proof of Concept exploratoire** et non un modèle de production.
> Les données FSBM ne sont pas incluses dans ce dépôt pour des raisons de confidentialité.

## 👥 Auteurs

| Étudiant            | Rôle                                   |
| ------------------- | -------------------------------------- |
| **ElGRIH Mohamed**  | Développement ML & Application         |
| **LAKHAL Youssef**  | Analyse de données & Modélisation      |
| **AKBI Mustapha**   | Déploiement & Documentation            |

**Encadrants** :
- Pr. ETTAOUFIK Abdelaziz — Encadrant académique (FSBM)
- Mr. Brahim Bella — Encadrant professionnel

**Établissement** : Faculté des Sciences Ben M'Sick — Université Hassan II Casablanca
**Filière** : Licence d'Excellence en Intelligence Artificielle
**Année universitaire** : 2025–2026
**Soutenance** : 22 Juin 2026

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2026 ElGRIH Mohamed, LAKHAL Youssef, AKBI Mustapha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**EduGuard AI** — *Prévoir le décrochage pour mieux le prévenir.*

</div>
