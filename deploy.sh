#!/bin/bash

# Script de déploiement Docker pour le bot Discord météo

echo "🚀 Déploiement du Bot Discord Météo avec Docker"
echo "=============================================="

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    echo "Téléchargez Docker depuis: https://docs.docker.com/get-docker/"
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Modifiez le fichier .env avec vos vraies clés API !"
    echo "   - DISCORD_TOKEN=votre_token_discord"
    echo "   - OPENWEATHER_API_KEY=votre_cle_api_openweathermap"
    echo ""
    read -p "Appuyez sur Entrée après avoir modifié le fichier .env..."
fi

# Créer le dossier data s'il n'existe pas
mkdir -p data

echo "🔨 Construction de l'image Docker..."
docker-compose build

echo "🚀 Démarrage du bot..."
docker-compose up -d

echo ""
echo "✅ Bot démarré avec succès !"
echo ""
echo "📊 Commandes utiles :"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter le bot: docker-compose down"
echo "  - Redémarrer le bot: docker-compose restart"
echo "  - Voir le statut: docker-compose ps"
echo ""
echo "🔍 Pour voir les logs en temps réel:"
echo "docker-compose logs -f discord-weather-bot"
