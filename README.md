# Bot Discord Météo 🌤️

Un bot Discord complet pour obtenir les prévisions météorologiques avec des graphiques interactifs, compatible avec py-cord.

## 🚀 Fonctionnalités

- **Météo actuelle** : Affiche la température, humidité et pression atmosphérique
- **Prévisions du jour** : Graphique des températures sur 24h
- **Prévisions de demain** : Graphique des températures du lendemain
- **Prévisions sur 5 jours** : Prévisions détaillées avec graphiques pour chaque jour
- **Interface moderne** : Embeds Discord avec icônes météo

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un bot Discord créé sur le [portail développeur Discord](https://discord.com/developers/applications)
- Une clé API OpenWeatherMap (gratuite sur [openweathermap.org](https://openweathermap.org/api))

## 🔧 Installation

### Option 1: Installation avec Docker (Recommandée) 🐳

```bash
# Cloner ou télécharger le projet
cd BotDiscordMeteo

# Configurer les variables d'environnement
cp .env.example .env
# Modifier .env avec vos vraies clés API

# Déployer avec Docker
./deploy.sh
```

### Option 2: Installation automatique (macOS/Linux)
```bash
chmod +x install.sh
./install.sh
```

### Option 3: Installation manuelle
```bash
# Installer les dépendances
pip3 install py-cord matplotlib requests

# Ou utiliser le fichier requirements.txt
pip3 install -r requirements.txt
```

## ⚙️ Configuration

1. **Configurer le bot Discord** :
   - Allez sur https://discord.com/developers/applications
   - Créez une nouvelle application
   - Dans la section "Bot", copiez le token

2. **Obtenir la clé API météo** :
   - Inscrivez-vous sur https://openweathermap.org/api
   - Copiez votre clé API

3. **Modifier le fichier config.py** :
```python
# Remplacez par vos vraies valeurs
TOKEN = "votre_token_discord_ici"
API = "votre_cle_api_openweathermap_ici"
```

## 🎮 Utilisation

### Avec Docker
```bash
# Démarrer le bot
./deploy.sh

# Voir les logs
docker-compose logs -f

# Arrêter le bot
docker-compose down
```

### Lancement traditionnel
```bash
python3 main.py
```

### Commandes disponibles

- `/command` - Affiche la liste des commandes
- `/meteo <ville>` - Météo actuelle d'une ville
- `/prevision <ville>` - Prévisions sur 24h avec graphique
- `/prevision-demain <ville>` - Prévisions de demain avec graphique
- `/prevision-semaine <ville>` - Prévisions sur 5 jours avec graphiques

### Exemples
```
/meteo Paris
/prevision Tokyo
/prevision-demain London
/prevision-semaine New York
```

## 🛠️ Compatibilité py-cord

Ce bot est entièrement compatible avec py-cord (version 2.4.0+) et inclut :

- ✅ Configuration correcte des intents
- ✅ Syntaxe des slash commands optimisée
- ✅ Gestion d'erreurs robuste
- ✅ Messages de suivi (followup) pour les prévisions longues
- ✅ Graphiques haute qualité avec matplotlib

## 📁 Structure du projet

```
BotDiscordMeteo/
├── main.py              # Code principal du bot
├── config.py            # Configuration (tokens, clés API)
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Configuration Docker
├── docker-compose.yml  # Orchestration Docker
├── .env.example        # Exemple de variables d'environnement
├── deploy.sh           # Script de déploiement Docker
├── install.sh          # Script d'installation traditionnelle
├── README.md           # Documentation
├── .dockerignore       # Fichiers ignorés par Docker
├── .gitignore          # Fichiers ignorés par Git
├── graphdemain.png     # Fichier temporaire pour les graphiques
└── Licence             # Licence du projet
```

## 🐳 Déploiement Docker

### Prérequis
- Docker et Docker Compose installés
- Variables d'environnement configurées dans `.env`

### Commandes Docker utiles
```bash
# Construire l'image
docker-compose build

# Démarrer en arrière-plan
docker-compose up -d

# Voir les logs en temps réel
docker-compose logs -f discord-weather-bot

# Redémarrer le service
docker-compose restart

# Arrêter et supprimer les conteneurs
docker-compose down

# Voir le statut des services
docker-compose ps
```

## 🔒 Sécurité

- Ne jamais commiter le fichier `config.py` avec vos vraies clés
- Gardez vos tokens et clés API secrets
- Utilisez des variables d'environnement en production

## 🐛 Dépannage

### Erreurs courantes

1. **ModuleNotFoundError: No module named 'discord'**
   ```bash
   pip3 install py-cord
   ```

2. **403 Forbidden (API OpenWeatherMap)**
   - Vérifiez que votre clé API est valide
   - Assurez-vous que votre plan API inclut les endpoints utilisés

3. **Bot ne répond pas aux commandes**
   - Vérifiez que le bot a les permissions nécessaires sur votre serveur
   - Assurez-vous que les slash commands sont bien synchronisées

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `Licence` pour plus de détails.

## 👨‍💻 Auteur

Développé par RaynhCoding

---

**Note** : Ce bot est conçu pour fonctionner avec py-cord, une fork moderne et maintenue de discord.py.

### <span style="color: #FFC300">Commands</span>
Affiche toute les commandes

### <span style="color: #FFC300">meteo</span>
Affiche l'état de la météo actuelle de la ville en paramètre

### <span style="color: #FFC300">prevision</span>
Affiche sous forme de graphique les températures sur 24h

### <span style="color: #FFC300">prevision-demain</span>
Affiche sous forme de graphique les températures entre 24h et 48h par rapport à l'heure où l'utilisateur entre la commande

### <span style="color: #FFC300">prevision-semaine<span>
Affiche sous forme de plusieurs graphes les températures pour 5 jours