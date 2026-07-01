# ========================================
# EduGuard AI — Dockerfile
# ========================================
# Image Python légère avec support Streamlit
#
# Build :   docker build -t eduguard-ai .
# Run   :   docker run -p 8501:8501 eduguard-ai
# Ou     :  docker-compose up --build

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="ElGRIH Mohamed, LAKHAL Youssef, AKBI Mustapha"
LABEL description="EduGuard AI — Système Intelligent de Prédiction du Décrochage Étudiant"
LABEL version="1.0.0"
LABEL license="MIT"

# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système minimales
# (libgomp1 nécessaire pour XGBoost, libgl1 pour matplotlib)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        libgl1 \
        libglib2.0-0 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copier d'abord requirements.txt pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application et les modèles
COPY app/ ./app/
COPY models/ ./models/
COPY models_fsmb/ ./models_fsmb/

# Créer un fichier .env par défaut (à override via docker-compose ou -e)
# Les valeurs par défaut sont les mots de passe de démo
ENV EDUGUARD_DEFAULT_PASSWORD=fsbm2025 \
    EDUGUARD_ADMIN_PASSWORD=admin2025

# Exposer le port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Lancer Streamlit
# --server.address=0.0.0.0 : écouter sur toutes les interfaces (requis dans Docker)
# --server.port=8501       : port par défaut
# --browser.gatherUsageStats=false : désactiver les stats d'usage
CMD ["streamlit", "run", "app/app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--browser.gatherUsageStats=false", \
     "--server.headless=true"]
