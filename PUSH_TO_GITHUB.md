# 🚀 Guide de publication sur GitHub — EduGuard AI

Ce guide explique pas à pas comment publier le projet EduGuard AI sur GitHub.

---

## 📋 Prérequis

1. **Compte GitHub** — créez-en un gratuitement sur https://github.com/signup
2. **Git installé** sur votre machine :
   - Windows : https://git-scm.com/download/win
   - macOS : `brew install git` ou https://git-scm.com/download/mac
   - Linux : `sudo apt install git` (Ubuntu/Debian)

Vérifiez l'installation :
```bash
git --version
```

---

## 1️⃣ Configurer Git (une seule fois sur votre machine)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Optionnel : mémoriser les identifiants (évite de les retaper)
git config --global credential.helper store
```

---

## 2️⃣ Créer le dépôt sur GitHub

1. Connectez-vous sur https://github.com
2. Cliquez sur le bouton **`+`** en haut à droite → **New repository**
3. Remplissez le formulaire :
   - **Repository name** : `EduGuard-AI`
   - **Description** : `Système Intelligent et Explicable de Prédiction Précoce du Décrochage Étudiant — PFE Licence d'Excellence IA, FSBM`
   - **Visibility** : ✅ **Public** (ou Private si vous préférez)
   - **Initialize this repository with** : ❌ NE COCHEZ RIEN
     (pas de README, pas de .gitignore, pas de LICENSE — on a déjà tout)
4. Cliquez sur **Create repository**

GitHub vous affiche une page avec des commandes. Gardez-la ouverte, on va les utiliser.

---

## 3️⃣ Préparer le dossier local

### Option A — Si vous avez le zip EduGuard-AI.zip

```bash
# Décompressez le zip où vous voulez
unzip EduGuard-AI.zip
cd EduGuard-AI
```

### Option B — Si vous avez le dossier directement

```bash
cd /chemin/vers/EduGuard-AI
```

---

## 4️⃣ Initialiser Git et faire le premier commit

Dans le dossier `EduGuard-AI`, exécutez :

```bash
# 1. Initialiser le dépôt Git local
git init

# 2. Renommer la branche principale en "main" (standard moderne)
git branch -M main

# 3. Vérifier que .env n'est PAS inclus (sécurité !)
# Doit afficher ".env" dans la liste
cat .gitignore | grep "\.env"

# 4. Ajouter tous les fichiers
git add .

# 5. Vérifier ce qui va être commit (IMPORTANT — vérifiez qu'il n'y a pas .env)
git status

# 6. Faire le premier commit
git commit -m "feat: initial release — EduGuard AI v1.0.0

Système Intelligent et Explicable de Prédiction Précoce du Décrochage Étudiant.

- Modèle XGBoost (76% accuracy, 0.914 AUC Dropout) sur dataset UCI (4424 étudiants, 36 features)
- Proof of Concept FSBM : Random Forest (84.6% accuracy) sur données marocaines (6009 étudiants, 6 features)
- Application web Streamlit avec prédiction individuelle + batch + SHAP explainability
- Docker + docker-compose pour déploiement containerisé
- Sécurité : mots de passe via .env (jamais dans config.yaml)

PFE — Licence d'Excellence en Intelligence Artificielle
FSBM — Université Hassan II Casablanca
Auteurs : ElGRIH Mohamed, LAKHAL Youssef, AKBI Mustapha"
```

---

## 5️⃣ Connecter au dépôt distant GitHub et pousser

Remplacez `VOTRE-USERNAME` par votre nom d'utilisateur GitHub :

```bash
# 1. Ajouter le dépôt distant
git remote add origin https://github.com/VOTRE-USERNAME/EduGuard-AI.git

# 2. Pousser le code sur GitHub
git push -u origin main
```

Git va vous demander vos identifiants GitHub :
- **Username** : votre nom d'utilisateur GitHub
- **Password** : utilisez un **Personal Access Token** (PAT), PAS votre mot de passe

### Créer un Personal Access Token (PAT)

1. Allez sur https://github.com/settings/tokens
2. Cliquez **Generate new token (classic)**
3. Donnez un nom (ex: `EduGuard AI push`)
4. Cochez **`repo`** (toutes les sous-options)
5. Cliquez **Generate token**
6. **COPIEZ LE TOKEN** (vous ne le verrez qu'une fois)
7. Utilisez ce token comme mot de passe lors du `git push`

---

## 6️⃣ Vérifier sur GitHub

1. Allez sur https://github.com/VOTRE-USERNAME/EduGuard-AI
2. Vérifiez que tous les fichiers sont là :
   - ✅ `app/` (avec `app.py`, `utils.py`, `pages/`, etc.)
   - ✅ `models/` (avec `model.json`, `scaler.pkl`, etc.)
   - ✅ `models_fsmb/`
   - ✅ `notebooks/` (avec `README.md` — à compléter)
   - ✅ `README.md` (affiché en page d'accueil)
   - ✅ `LICENSE` (MIT)
   - ✅ `Dockerfile` + `docker-compose.yml`
   - ✅ `requirements.txt`
   - ❌ `.env` NE DOIT PAS apparaître (sécurité)

---

## 7️⃣ Ajouter les notebooks Colab (à faire plus tard)

Les notebooks ne sont pas inclus par défaut. Pour les ajouter :

```bash
# 1. Téléchargez les notebooks depuis Google Drive
# (dossier PFE_Dropout/notebooks/)

# 2. Placez-les dans le dossier notebooks/
#    - 01_exploration.ipynb
#    - 02_preprocessing.ipynb
#    - 03_modeling.ipynb
#    - 04_evaluation_shap.ipynb

# 3. Ajoutez-les à Git
git add notebooks/

# 4. Committez
git commit -m "docs: add Google Colab notebooks (EDA, preprocessing, modeling, evaluation)"

# 5. Poussez
git push
```

---

## 8️⃣ Ajouter des sujets (tags) au repo

Sur la page GitHub du repo :
1. Cliquez sur ⚙️ (About) en haut à droite
2. Ajoutez les topics :
   ```
   machine-learning  xgboost  shap  streamlit  student-dropout
   education  artificial-intelligence  pfe  fsbm  morocco
   python  scikit-learn  smote  explainable-ai
   ```
3. Ajoutez une description et un site web (optionnel)
4. Cliquez **Save changes**

---

## 9️⃣ Workflow quotidien (pour les futures modifications)

```bash
# Modifier des fichiers...

# Voir ce qui a changé
git status
git diff

# Ajouter les modifications
git add .

# Committer avec un message clair
git commit -m "fix: corrige le calcul du seuil de risque"
# ou
git commit -m "feat: ajoute l'export PDF des résultats"
# ou
git commit -m "docs: met à jour le README"

# Pousser sur GitHub
git push
```

### Convention de messages (Conventional Commits)

| Préfixe  | Usage                                         |
| -------- | --------------------------------------------- |
| `feat:`  | Nouvelle fonctionnalité                      |
| `fix:`   | Correction de bug                             |
| `docs:`  | Documentation (README, commentaires)         |
| `style:` | Formatage, espaces, points-virgules          |
| `refactor:` | Refactorisation sans changement de comportement |
| `test:`  | Ajout/modification de tests                   |
| `chore:` | Tâches de maintenance (dépendances, etc.)    |

---

## 🔁 Inviter les coéquipiers (optionnel)

Si Lakhal Youssef et AKBI Mustapha doivent aussi push :

1. Sur GitHub : **Settings → Collaborators → Add people**
2. Entrez leurs usernames GitHub
3. Ils recevront une invitation par email
4. Ils devront faire un `git clone` du repo, puis pourront push après avoir fait des commits

---

## 🌐 Activer GitHub Pages (optionnel — pour une démo en ligne)

Pour héberger une démo de l'app avec Streamlit Cloud (gratuit) :

1. Allez sur https://share.streamlit.io
2. Connectez-vous avec GitHub
3. **New app** → sélectionnez `VOTRE-USERNAME/EduGuard-AI`
4. **Main file path** : `app/app.py`
5. **Requirements** : `requirements.txt`
6. Cliquez **Deploy**

L'app sera accessible sur `https://votre-username-eduguard-ai.streamlit.app`

---

## 🆘 Dépannage

### `git push` demande un mot de passe qui ne marche pas

→ Utilisez un **Personal Access Token** (PAT), pas votre mot de passe GitHub.
Voir étape 5 ci-dessus.

### `! [rejected] main -> main (fetch first)` lors du push

→ Quelqu'un d'autre a push des changements. Faites :
```bash
git pull --rebase origin main
git push
```

### `fatal: remote origin already exists`

→ Le remote existe déjà. Pour le changer :
```bash
git remote set-url origin https://github.com/VOTRE-USERNAME/EduGuard-AI.git
```

### Les fichiers `.pkl` sont trop gros pour GitHub (>100MB)

→ Utilisez **Git LFS** :
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m "chore: configure Git LFS for .pkl files"
git push
```

### J'ai commité `.env` par erreur !

→ Retirez-le immédiatement :
```bash
git rm --cached .env
git commit -m "security: remove .env from tracking"
git push
# CHANGEZ TOUS LES MOTS DE PASSE — ils sont dans l'historique Git !
```

---

## ✅ Checklist finale

- [ ] Git installé et configuré (`user.name`, `user.email`)
- [ ] Dépôt créé sur GitHub (`EduGuard-AI`, Public)
- [ ] `git init` + `git add .` + `git commit` fait en local
- [ ] `git remote add origin` + `git push -u origin main` réussi
- [ ] `.env` n'apparaît PAS sur GitHub (vérifiez !)
- [ ] README affiché correctement sur la page d'accueil GitHub
- [ ] Topics ajoutés au repo
- [ ] (Optionnel) Notebooks ajoutés
- [ ] (Optionnel) App déployée sur Streamlit Cloud
- [ ] (Optionnel) Coéquipiers invités comme collaborateurs

---

**Félicitations ! 🎉 Votre PFE est maintenant sur GitHub.**

N'oubliez pas d'ajouter le lien du repo sur votre **LinkedIn** et votre **CV** !
