# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires pour matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application
COPY . .

# Créer un utilisateur non-root pour exécuter l'application
RUN useradd --create-home --shell /bin/bash botuser
RUN chown -R botuser:botuser /app
USER botuser

# Exposer le port (optionnel, pour les métriques futures)
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "main.py"]
