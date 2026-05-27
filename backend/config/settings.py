# =========================================================
# settings.py
# =========================================================
#
# Ce fichier centralise toute la configuration globale
# du projet.
#
# Son rôle :
#
# - charger les variables du .env
# - convertir les valeurs correctement
# - exposer des constantes réutilisables
#
# IMPORTANT :
#
# Aucun autre fichier du projet ne devrait utiliser
# directement os.getenv().
#
# Toute la configuration doit passer par settings.py.
#
# =========================================================
#
# Exemple d'import :
#
# from config.settings import (
#     USE_OLLAMA,
#     USE_OPENAI,
#     USE_VISION
# )
#
# =========================================================


import os
from dotenv import load_dotenv
from config.toggle import env_bool


# =========================================================
# Chargement du fichier .env
# =========================================================

load_dotenv()

# =========================================================
# Modèle Ollama utilisé par défaut
# =========================================================
#
# Exemple dans .env :
#
# OLLAMA_MODEL=llama3
#
# Si aucune valeur n'existe :
#
# "llama3" sera utilisé.
#
# =========================================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)

# =========================================================
# Active/désactive Ollama
# =========================================================
#
# Exemple :
#
# USE_OLLAMA=true
#
# Si la variable n'existe pas :
#
# default=True
#
# donc Ollama sera activé par défaut.
# =========================================================

USE_OLLAMA = env_bool(
    os.getenv("USE_OLLAMA"),
    default=True
)


# =========================================================
# Active/désactive OpenAI
# =========================================================

# USE_OPENAI = env_bool(
#     os.getenv("USE_OPENAI"),
#     default=False
# )


# =========================================================
# Active/désactive les fonctionnalités vision
# =========================================================
#
# Exemple :
#
# analyse d'image
# OCR
# image captioning
# modèles multimodaux
#
# =========================================================

USE_VISION = env_bool(
    os.getenv("USE_VISION"),
    default=False
)


# =========================================================
# Active/désactive les fonctionnalités audio
# =========================================================
#
# Exemple :
#
# reconnaissance vocale
# synthèse vocale
# voice assistant
#
# =========================================================

USE_AUDIO = env_bool(
    os.getenv("USE_AUDIO"),
    default=False
)


