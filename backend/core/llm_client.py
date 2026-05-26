# Client LLM universel 

# =========================================================
# Activation des providers IA via variables d'environnement
# =========================================================
#
# Ces variables permettent d'activer ou désactiver
# dynamiquement un provider LLM.
#
# Exemple dans le fichier .env :
#
# USE_OLLAMA=true
# USE_OPENAI=false
# USE_MISTRAL=false
# # exemple d'import de models : from config.settings import USE_OLLAMA
# Il est recommandé d'utiliser env_bool()
# pour une gestion plus robuste des booléens.
# =========================================================

import os
import requests
from openai import OpenAI
from mistralai.client import MistralClient


USE_OLLAMA = os.getenv("USE_OLLAMA") == "true"
USE_OPENAI = os.getenv("USE_OPENAI") == "true"
USE_MISTRAL = os.getenv("USE_MISTRAL") == "true"

# =========================================================
# Classe principale de gestion des LLM
# =========================================================
#
# Cette classe agit comme une abstraction des providers IA.
#
# Elle permet :
#
# - d'utiliser Ollama en local
# - d'utiliser OpenAI
# - d'utiliser Mistral
# - de changer de provider sans modifier le reste du code
#
# Le backend n'appelle qu'une seule méthode :
#
# client.ask(prompt)
#
# Puis le provider approprié est choisi automatiquement.
# =========================================================
class LLMClient:

    # =====================================================
    # Méthode principale appelée par le backend
    # =====================================================
    #
    # Paramètres :
    #
    # prompt (str)
    # → texte envoyé au modèle IA
    #
    # Retour :
    #
    # str
    # → réponse générée par le provider sélectionné
    # =====================================================
    def ask(self, prompt: str):

        # =================================================
        # Provider Ollama local
        # =================================================
        #
        # Si USE_OLLAMA=true dans le .env
        # alors la requête est envoyée au serveur Ollama.
        # =================================================
        if USE_OLLAMA:
            return self.ask_ollama(prompt)

        if USE_OPENAI:
            return self.ask_openai(prompt)

        if USE_MISTRAL:
            return self.ask_mistral(prompt)

        return "No provider enabled"

    # =====================================================
    # Appel du serveur Ollama local
    # =====================================================
    #
    # Cette méthode communique avec l'API HTTP d'Ollama.
    #
    # URL par défaut :
    #
    # http://localhost:11434
    #
    # Endpoint utilisé :
    #
    # /api/generate
    #
    # Paramètres envoyés :
    #
    # - model :
    #   modèle Ollama utilisé
    #
    # - prompt :
    #   texte envoyé au modèle
    #
    # - stream :
    #   False = réponse complète
    #   True  = streaming token par token
    #
    # Retour :
    #
    # str
    # → texte généré par Ollama
    # =====================================================
    def ask_ollama(self, prompt):
        # Requête HTTP POST vers Ollama avec le modèle utilisé, le prompts et le streaming : False :→ réponse complète d'un coup / True : → réponse token par token
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]