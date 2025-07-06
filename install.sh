#!/bin/bash

# Script d'installation pour le bot Discord météo
echo "Installation des dépendances pour le bot Discord météo..."

# Vérifier si Python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "Erreur: Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Installer les dépendances
echo "Installation de py-cord..."
pip3 install py-cord

echo "Installation de matplotlib..."
pip3 install matplotlib

echo "Installation de requests..."
pip3 install requests

echo ""
echo "Installation terminée !"
echo ""
echo "Pour configurer le bot :"
echo "1. Modifiez le fichier config.py avec vos tokens/clés API"
echo "2. Lancez le bot avec: python3 main.py"
echo ""
echo "N'oubliez pas de :"
echo "- Créer une application Discord sur https://discord.com/developers/applications"
echo "- Obtenir une clé API OpenWeatherMap sur https://openweathermap.org/api"
