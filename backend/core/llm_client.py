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

import httpx
# from openai import OpenAI
# from mistralai.client import MistralClient
from config.settings import USE_OLLAMA, OLLAMA_MODEL


# Cette classe agit comme une abstraction des providers IA.
class LLMClient:

    # → réponse générée par le provider sélectionné
    def ask(self, prompt: str):

        # Provider Ollama local
        if USE_OLLAMA:
            return self.ask_ollama(prompt)

        # if USE_OPENAI:
        #     return self.ask_openai(prompt)

        # if USE_MISTRAL:
        #     return self.ask_mistral(prompt)

        return "No provider enabled"


    # Cette méthode communique avec l'API HTTP d'Ollama.
    def ask_ollama(self, prompt: str) -> str:
        # Requête HTTP POST vers Ollama avec le modèle utilisé, le prompts et le streaming : False :→ réponse complète d'un coup / True : → réponse token par token
        try:
            response = httpx.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["response"]

        except Exception as e:
            print(f"⚠️ Ollama error: {e}")
            return "Erreur : impossible de contacter Ollama."