# Guide Complet — Créer un Bundle de Chatbots Réutilisables

## Objectif

Créer une architecture de chatbot moderne, modulaire et réutilisable basée sur :

* Frontend React + Vite
* Backend FastAPI
* Ollama (local)
* Switch OpenAI / Mistral / Ollama
* Analyse d'image
* Analyse vocale
* Recherche locale de fichiers
* Système de prompts versionnés
* Architecture multi-bots
* Mode démo configurable

Ce guide est conçu comme un cours étape par étape.

---

# 1. Architecture finale du projet

```txt
chatbot_bundle/
│
├── backend/
│   ├── core/
│   ├── bots/
│   ├── api/
│   ├── prompts/
│   ├── services/
│   ├── models/
│   ├── config/
│   ├── tests/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── services/
│   └── App.jsx
│
├── data/
├── scripts/
├── docker/
├── .env
├── requirements.txt
└── README.md
```


🧠 Règle simple pour ton architecture
- core/ → cerveau (IA, orchestration, logique centrale)
- services/ → outils externes (API, DB, stockage)
- bots/ → comportements spécialisés
- api/ → exposition HTTP


---

# 2. Technologies utilisées

## Frontend

| Technologie         | Usage             |
| ------------------- | ----------------- |
| React               | Interface chatbot |
| Vite                | Build rapide      |
| TailwindCSS         | UI moderne        |
| Axios               | Requêtes API      |
| Zustand (optionnel) | State global      |
| Tauri (optionnel)   | App desktop       |

---

## Backend

| Technologie  | Usage                 |
| ------------ | --------------------- |
| FastAPI      | API backend           |
| Pydantic     | Validation            |
| Uvicorn      | Serveur               |
| Ollama       | LLM local             |
| OpenAI SDK   | GPT                   |
| Mistral SDK  | Mistral               |
| Transformers | IA locale             |
| Pillow       | Traitement image      |
| Vosk         | Reconnaissance vocale |
| pyttsx3      | Synthèse vocale       |

---

# 3. Installation du projet

## Installer Python

Télécharger :

* [https://www.python.org/downloads/](https://www.python.org/downloads/)

Vérifier :

```bash
python --version
```

---

## Installer Node.js

Télécharger :

* [https://nodejs.org/](https://nodejs.org/)

Vérifier :

```bash
node -v
npm -v
```

---

# 4. Installer Ollama

## Télécharger

* [https://ollama.com/](https://ollama.com/)

---

## Installer un modèle

```bash
ollama pull llama3
```

Autres modèles :

```bash
ollama pull mistral
ollama pull phi3
ollama pull gemma
```

---

## Tester Ollama

```bash
ollama run llama3
```

---

# 5. Création du backend FastAPI

## Initialisation

```bash
mkdir chatbot_bundle
cd chatbot_bundle
mkdir backend
cd backend
```

---

## Créer l'environnement virtuel

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 6. Installer les dépendances backend

```bash
pip install fastapi uvicorn pydantic requests python-dotenv
```

---

## Support OpenAI

```bash
pip install openai
```

---

## Support Mistral

```bash
pip install mistralai
```

---

## Analyse IA locale

```bash
pip install transformers torch
```

---

## Vision

```bash
pip install pillow
```

---

## Audio

```bash
pip install vosk pyttsx3 sounddevice
```

---

## Ajouter les dépendances au fichier requirements.txt
Ajouter tout les paquets installé précédemment dans le fichier.

Puis les installer :
```shell
pip install -r requirements.txt
```


# 7. Fichier .env

Créer :

```txt
backend/.env
```

---

## Exemple

```env
USE_OLLAMA=true
USE_OPENAI=false
USE_MISTRAL=false

OLLAMA_MODEL=llama3

OPENAI_API_KEY=xxxxx
MISTRAL_API_KEY=xxxxx

USE_DEMO_MODE=false
USE_VISION=true
USE_VOICE=true
```

---

# 8. Core réutilisable

## Structure du core

```txt
core/
├── llm_client.py
├── prompt_manager.py
├── toggle.py
├── schema.py
├── vision.py
├── voice.py
├── sentiment.py
└── file_search.py
```

---

# 9. Gestion des toggles et de la configuration

## config/ setting

```python
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


# =========================================================
# Import système
# =========================================================

import os


# =========================================================
# Chargement automatique du fichier .env
# =========================================================
#
# load_dotenv() permet de charger les variables
# d'environnement définies dans :
#
# .env
#
# Exemple :
#
# USE_OLLAMA=true
# OLLAMA_MODEL=llama3
#
# =========================================================

from dotenv import load_dotenv


# =========================================================
# Import du helper de conversion booléenne
# =========================================================

from config.toggle import env_bool


# =========================================================
# Chargement du fichier .env
# =========================================================

load_dotenv()


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

USE_OPENAI = env_bool(
    os.getenv("USE_OPENAI"),
    default=False
)


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
```


## toggle.py
Créer un fichier toggle.py dans le dossier config.
```python
# =========================================================
# toggle.py
# =========================================================
#
# Ce fichier contient des helpers utilitaires permettant
# de convertir des variables d'environnement en booléens.
#
# Pourquoi ?
#
# Les variables d'environnement sont toujours lues
# sous forme de chaînes de caractères :
#
# "true"
# "false"
# "1"
# "0"
#
# et non comme de vrais booléens Python.
#
# Ce helper permet :
#
# - d'éviter les bugs
# - de centraliser la logique de conversion
# - de rendre le .env flexible
# - d'avoir un système de toggles propre
#
# Exemple :
#
# USE_OLLAMA=true
# USE_VISION=no
#
# deviennent :
#
# True
# False
#
# =========================================================


# =========================================================
# Valeurs considérées comme True
# =========================================================
#
# Toutes les valeurs de cet ensemble seront converties
# en True.
#
# Exemple :
#
# "true"
# "1"
# "yes"
# "on"
#
# =========================================================

TRUE_SET = {"1", "true", "yes", "on"}


# =========================================================
# Valeurs considérées comme False
# =========================================================
#
# Toutes les valeurs de cet ensemble seront converties
# en False.
#
# Exemple :
#
# "false"
# "0"
# "no"
# "off"
#
# =========================================================

FALSE_SET = {"0", "false", "no", "off"}


# =========================================================
# Convertit une variable d'environnement en booléen
# =========================================================
#
# Paramètres :
#
# value :
# → valeur récupérée depuis os.getenv()
#
# default :
# → valeur retournée si :
#   - la variable n'existe pas
#   - la valeur est invalide
#
# Retour :
#
# bool
#
# =========================================================
#
# Exemple :
#
# env_bool("true")  -> True
# env_bool("false") -> False
# env_bool("yes")   -> True
# env_bool(None)    -> default
#
# =========================================================

def env_bool(value: str | None, default: bool = False) -> bool:


    # =====================================================
    # Cas où la variable n'existe pas
    # =====================================================
    #
    # os.getenv() peut retourner None si la variable
    # n'est pas définie dans le .env.
    #
    # Dans ce cas :
    #
    # on retourne la valeur par défaut.
    # =====================================================

    if value is None:
        return default


    # =====================================================
    # Normalisation de la chaîne
    # =====================================================
    #
    # strip()
    # → supprime les espaces inutiles
    #
    # lower()
    # → transforme en minuscule
    #
    # Exemple :
    #
    # " TRUE "
    #
    # devient :
    #
    # "true"
    # =====================================================

    v = value.strip().lower()


    # =====================================================
    # Vérifie si la valeur correspond à True
    # =====================================================

    if v in TRUE_SET:
        return True


    # =====================================================
    # Vérifie si la valeur correspond à False
    # =====================================================

    if v in FALSE_SET:
        return False


    # =====================================================
    # Valeur invalide ou inconnue
    # =====================================================
    #
    # Exemple :
    #
    # env_bool("bonjour")
    #
    # Retourne la valeur par défaut.
    # =====================================================

    return default
```

---

# 10. Gestion des prompts

## prompt_manager.py

```python
from pathlib import Path

PROMPT_DIR = Path("prompts")


def load_prompt(name: str):
    path = PROMPT_DIR / name
    return path.read_text(encoding="utf-8")
```

---

# 11. Client LLM universel

## llm_client.py

Architecture importante :

* Un seul client
* Plusieurs providers
* Switch automatique

Activation des providers IA via variables d'environnement
Ces variables permettent d'activer ou désactiver
 dynamiquement un provider LLM.

 Exemple dans le fichier .env :
* USE_OLLAMA=true
* USE_OPENAI=false
* USE_MISTRAL=false

***exemple d'import de models : from config.settings import USE_OLLAMA***

Il est recommandé d'utiliser env_bool() pour une gestion plus robuste des booléens (voir settings.py).

---

## Exemple simplifié

```python
# =========================================================
# Client LLM universel
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
# Puis le provider approprié est choisi automatiquement
# selon les variables d'environnement définies
# dans le fichier .env.
#
# Exemple :
#
# USE_OLLAMA=true
# USE_OPENAI=false
# USE_MISTRAL=false
#
# Le modèle Ollama utilisé peut aussi être configuré :
#
# OLLAMA_MODEL=llama3
# =========================================================

import httpx

# from openai import OpenAI
# from mistralai.client import MistralClient

# =========================================================
# Import des paramètres globaux
# =========================================================
#
# USE_OLLAMA :
# → active ou désactive Ollama
#
# OLLAMA_MODEL :
# → modèle Ollama utilisé pour les générations
# =========================================================
from config.settings import USE_OLLAMA, OLLAMA_MODEL


# =========================================================
# Classe principale de gestion des LLM
# =========================================================
#
# Cette classe sert de couche d'abstraction entre
# le backend et les différents providers IA.
#
# L'objectif est de centraliser :
#
# - le choix du provider
# - les appels API
# - la gestion des erreurs
#
# afin de garder le reste du projet indépendant
# du provider utilisé.
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
    #
    # Fonctionnement :
    #
    # - vérifie quel provider est activé
    # - route automatiquement la requête
    # - retourne la réponse générée
    # =====================================================
    def ask(self, prompt: str):

        # =================================================
        # Provider Ollama local
        # =================================================
        #
        # Si USE_OLLAMA=true dans le .env,
        # la requête est envoyée au serveur Ollama local.
        # =================================================
        if USE_OLLAMA:
            return self.ask_ollama(prompt)

        # =================================================
        # Future intégration OpenAI
        # =================================================
        #
        # if USE_OPENAI:
        #     return self.ask_openai(prompt)
        # =================================================

        # =================================================
        # Future intégration Mistral
        # =================================================
        #
        # if USE_MISTRAL:
        #     return self.ask_mistral(prompt)
        # =================================================

        # Aucun provider activé
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
    # Timeout :
    #
    # 60 secondes maximum
    #
    # Retour :
    #
    # str
    # → texte généré par Ollama
    #
    # Gestion des erreurs :
    #
    # - capture les erreurs réseau
    # - capture les erreurs HTTP
    # - évite de faire planter le backend
    # =====================================================
    def ask_ollama(self, prompt: str) -> str:

        try:

            # =================================================
            # Requête HTTP POST vers Ollama
            # =================================================
            response = httpx.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )

            # =================================================
            # Vérifie si la requête HTTP est valide
            # =================================================
            response.raise_for_status()

            # =================================================
            # Extraction de la réponse générée
            # =================================================
            return response.json()["response"]

        # =====================================================
        # Gestion globale des erreurs
        # =====================================================
        except Exception as e:

            print(f"⚠️ Ollama error: {e}")

            return "Erreur : impossible de contacter Ollama."
```

---

# 12. Schémas Pydantic

## schema.py

```python
# =====================================================
# Schemas Pydantic utilises par l'API.
# =====================================================

# Pydantic garantit :
# - la structure des données,
# - la validation automatique,
# - des échanges frontend/backend fiables.

# Un schema sert a definir clairement :
# - ce que l'API attend en entree
# - ce qu'elle renvoie en sortie

# FastAPI s'appuie dessus pour :
# - valider les donnees recues
# - documenter automatiquement l'API dans /docs

from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
```

---

# 13. Création du moteur de chat
Créer le fichier dans : backend/core/chat_engine.py

## chat_engine.py

Ce fichier contient le moteur principal du chatbot.

Son rôle :
 - recevoir les messages utilisateur
 - construire le prompt envoyé au LLM
 - appeler le provider IA
 - retourner la réponse générée

 > Ce moteur agit comme une couche intermédiaire entre :

> Frontend/API
    ↓
ChatEngine
    ↓
 LLMClient
    ↓
 Ollama / OpenAI / Mistral

> Import du client LLM universel

LLMClient est une abstraction des providers IA.

Il permet de :
- utiliser Ollama
- utiliser OpenAI
- utiliser Mistral
 sans modifier le reste du projet.


```python
# =====================================================
# Moteur principal du chatbot
# =====================================================
#
# ChatEngine orchestre la conversation entre
# l'utilisateur et le modèle IA.
#
# Il gère :
#
# - le prompt système (personnalité du bot)
# - l'historique de la conversation
# - l'envoi des messages au provider LLM
#
# =====================================================

from core.llm_client import LLMClient
from core.prompt_manager import load_prompt


class ChatEngine:


    # =================================================
    # Constructeur
    # =================================================
    #
    # Initialise le moteur de conversation.
    #
    # - charge le prompt système depuis un fichier
    # - prépare un historique vide
    # - instancie le client LLM
    #
    # =================================================

    def __init__(self):

        self.client = LLMClient()


        # =============================================
        # Prompt système
        # =============================================
        #
        # Définit la personnalité et les instructions
        # de base du chatbot.
        #
        # Chargé depuis :
        #
        # prompts/exemple_v1.0.txt
        #
        # =============================================

        self.system_prompt = load_prompt("exemple_v1.0.txt")


        # =============================================
        # Historique de la conversation
        # =============================================
        #
        # Liste des échanges au format :
        #
        # "User: ..."
        # "Assistant: ..."
        #
        # Permet au modèle de garder le contexte
        # des messages précédents.
        #
        # =============================================

        self.history = []


    # =================================================
    # Méthode principale de conversation
    # =================================================
    #
    # Paramètres :
    #
    # message (str)
    # → message envoyé par l'utilisateur
    #
    # Retour :
    #
    # str
    # → réponse générée par le LLM
    #
    # =================================================

    def chat(self, message: str):


        # =============================================
        # Ajout du message utilisateur à l'historique
        # =============================================
        #
        # On préfixe avec "User:" pour que le modèle
        # comprenne qui parle.
        #
        # =============================================

        self.history.append(f"User: {message}")


        # =============================================
        # Construction du prompt complet
        # =============================================
        #
        # Le prompt final envoyé au modèle est composé
        # de trois parties :
        #
        # 1. system_prompt  → personnalité du bot
        # 2. conversation   → historique des échanges
        # 3. "Assistant:"   → invite le modèle à répondre
        #
        # Exemple :
        #
        # Tu es un assistant utile...
        #
        # User: Bonjour
        # Assistant: Bonjour ! Comment puis-je...
        # User: Explique FastAPI
        # Assistant:
        #
        # =============================================

        conversation = "\n".join(self.history)
        prompt = f"{self.system_prompt}\n\n{conversation}\nAssistant:"


        # =============================================
        # Envoi du prompt au provider LLM
        # =============================================
        #
        # self.client.ask() envoie le prompt à :
        #
        # - Ollama
        # - ou OpenAI
        # - ou Mistral
        #
        # selon la configuration active dans .env
        #
        # =============================================

        reply = self.client.ask(prompt)


        # =============================================
        # Ajout de la réponse à l'historique
        # =============================================
        #
        # On préfixe avec "Assistant:" pour que les
        # prochains échanges gardent le contexte.
        #
        # =============================================

        self.history.append(f"Assistant: {reply}")

        return reply
```

---

# 14. API FastAPI

## main.py

Ce fichier représente le point d'entrée principal du backend FastAPI.

Son rôle :

 - créer l'application FastAPI
 - initialiser le moteur du chatbot
 - exposer les routes API
 - recevoir les requêtes frontend
 - retourner les réponses du LLM
  
Architecture :
    Frontend React
        ↓
    API FastAPI
        ↓
    ChatEngine
        ↓
    LLMClient
        ↓
    Ollama / OpenAI / Mistral

```python
# =========================================================
# Import FastAPI
# =========================================================
#
# FastAPI est le framework backend utilisé
# pour créer les routes API du chatbot.
#
# =========================================================

from fastapi import FastAPI


# =========================================================
# Import du moteur principal du chatbot
# =========================================================
#
# ChatEngine :
#
# - construit les prompts
# - appelle le provider IA
# - retourne les réponses générées
#
# =========================================================

from core.chat_engine import ChatEngine


# =========================================================
# Import des schémas Pydantic
# =========================================================
#
# ChatRequest sert à :
#
# - valider automatiquement les requêtes JSON
# - typer les données reçues
# - sécuriser les entrées API
#
# =========================================================

from core.schema import ChatRequest


# =========================================================
# Import du middleware CORS
# =========================================================
#
# CORSMiddleware permet de gérer les requêtes cross-origin (CORS)
#
#  CORS = autoriser un frontend (React, Vue, etc.)
#          à appeler ton backend FastAPI
#
# Sans ce middleware, le navigateur bloque les requêtes
# venant d’un autre domaine / port (ex: localhost:5173 → localhost:8000)
#
# =========================================================

from fastapi.middleware.cors import CORSMiddleware

# =========================================================
# Création de l'application FastAPI
# =========================================================
#
# Cette instance représente l'API backend complète.
#
# Toutes les routes seront attachées à cet objet.
#
# =========================================================

app = FastAPI()


# =========================================================
# Initialisation du moteur chatbot
# =========================================================
#
# Une seule instance est créée au démarrage
# du backend.
#
# Cette instance sera réutilisée pour toutes
# les requêtes utilisateur.
#
# =========================================================

engine = ChatEngine()

# =========================================================
# Configuration du middleware CORS
# =========================================================
#
# app.add_middleware() ajoute un middleware global à l'application FastAPI
#
# Ici on configure les règles d'accès à l'API
#
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # -----------------------------------------------------
    # allow_origins
    # -----------------------------------------------------
    #
    # Liste des domaines autorisés à accéder à l'API
    #
    # "*" = tous les domaines sont autorisés
    #
    # ⚠️ En production, il est recommandé de restreindre :
    # ["https://mon-site.com"]
    #
    allow_origins=["http://localhost:5173"],

    # -----------------------------------------------------
    # allow_credentials
    # -----------------------------------------------------
    #
    # Autorise l'envoi de cookies et identifiants (auth)
    #
    # Nécessaire si tu utilises :
    # - JWT en cookies
    # - sessions utilisateur
    #
    allow_credentials=True,

    # -----------------------------------------------------
    # allow_methods
    # -----------------------------------------------------
    #
    # Liste des méthodes HTTP autorisées
    #
    # "*" = toutes les méthodes sont autorisées :
    # GET, POST, PUT, DELETE, PATCH, etc.
    #
    allow_methods=["*"],

    # -----------------------------------------------------
    # allow_headers
    # -----------------------------------------------------
    #
    # Liste des headers HTTP autorisés
    #
    # "*" = tous les headers sont acceptés
    #
    # Exemples de headers :
    # - Authorization
    # - Content-Type
    # - Accept
    #
    allow_headers=["*"],
)

# =========================================================
# Route API : Route de test simple.
# =========================================================
#Elle permet de verifier rapidement que l'API repond bien.

@app.get("/")
def home():
    return {"message": "API chatbot OK"}

# =========================================================
# Route API principale du chatbot
# =========================================================
#
# Endpoint :
#
# POST /chat
#
# Cette route :
#
# 1. reçoit les messages du frontend
# 2. extrait le dernier message utilisateur
# 3. envoie le message au ChatEngine
# 4. récupère la réponse IA
# 5. retourne la réponse au frontend
#
# =========================================================

@app.post("/chat")


# =========================================================
# Fonction appelée lorsqu'une requête arrive
# sur /chat
# =========================================================
#
# Paramètres :
#
# req : ChatRequest -> défini dans schema.py
#
# Exemple JSON reçu :
#
# {
#   "messages": [
#       {
#           "role": "user",
#           "content": "Bonjour"
#       }
#   ]
# }
#
# FastAPI + Pydantic convertissent automatiquement
# ce JSON en objet Python typé.
#
# =========================================================

def chat(req: ChatRequest):


    # =====================================================
    # Récupération du dernier message utilisateur
    # =====================================================
    #
    # req.messages :
    # → liste des messages de conversation
    #
    # [-1] :
    # → dernier élément de la liste
    #
    # .content :
    # → texte du message
    #
    # Exemple :
    #
    # "Bonjour"
    #
    # =====================================================

    user_message = req.messages[-1].content


    # =====================================================
    # Envoi du message au moteur IA
    # =====================================================
    #
    # Le ChatEngine :
    #
    # - construit le prompt
    # - appelle Ollama/OpenAI/Mistral
    # - récupère la réponse générée
    #
    # =====================================================

    reply = engine.chat(user_message)


    # =====================================================
    # Retour de la réponse au frontend
    # =====================================================
    #
    # FastAPI convertit automatiquement ce dictionnaire
    # Python en JSON.
    #
    # Exemple retourné :
    #
    # {
    #   "reply": "Bonjour !"
    # }
    #
    # =====================================================

    return {
        "reply": reply
    }
```

### Créer un prompt

Dans le dossier prompt du backend, créer un fichier de type "exemple_v1.0.txt".
Mettre le prompt de ce que l'on veut générer.

Il est géré par le /core/prompt_manager.py

---

# 15. Lancer le backend

```bash
uvicorn main:app --reload
```

API :

```txt
http://127.0.0.1:8000/docs
```

---

# 16. Création du frontend React

## Initialisation

```bash
npm create vite@latest frontend
```

Choisir :

```txt
React
JavaScript
```

---

## Installer les dépendances

```bash
cd frontend
npm install
npm install axios 
```
Axios est installé principalement pour simplifier les appels API entre React et FastAPI
---

# 17. Installation Tailwind

Autoprefixer est installé avec TailwindCSS pour ajouter automatiquement les préfixes CSS nécessaires selon les navigateurs

```bash
npm install tailwindcss @tailwindcss/vite
```

---

## Configuration de vite

Dans vite.config.js

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

Ajouter Tailwind dans le src/index.css

```css
@import "tailwindcss";
```

Importer le CSS dans main.jsx

```js
import './index.css'
```

Puis lancer le frontend :

`npm run dev`


---

# 18. Chat UI

## App.jsx

Ce composant représente l'interface principale
du chatbot React.
* Son rôle :
- afficher les messages
- gérer l'état de la conversation
- envoyer les requêtes au backend FastAPI
- afficher les réponses du LLM
 
> ***Architecture :***
> 
> React Frontend
    ↓ 
axios HTTP
FastAPI Backend
    ↓
ChatEngine
    ↓
Ollama / OpenAI / Mistral

```jsx
// =========================================================
// Import du hook React useState
// =========================================================
//
// useState permet de stocker des données dynamiques
// dans le composant.
//
// Ici il sert à gérer :
//
// - les messages du chat
// - le texte de l'input utilisateur
//
// =========================================================

import { useState } from "react"


// =========================================================
// Import d'Axios
// =========================================================
//
// Axios permet d'envoyer des requêtes HTTP
// vers le backend FastAPI.
//
// Ici :
//
// React → POST /chat → FastAPI
//
// =========================================================

import axios from "axios"



// =========================================================
// Composant principal React
// =========================================================
//
// Ce composant contient :
//
// - l'UI du chatbot
// - l'état de la conversation
// - l'envoi des messages
//
// =========================================================

function App() {

  // =======================================================
  // État des messages du chatbot
  // =======================================================
  //
  // messages :
  // → tableau contenant toute la conversation
  //
  // setMessages :
  // → fonction permettant de modifier les messages
  //
  // Exemple :
  //
  // [
  //   {
  //      role: "user",
  //      content: "Bonjour"
  //   },
  //   {
  //      role: "assistant",
  //      content: "Bonjour humain."
  //   }
  // ]
  //
  // =======================================================

  const [messages, setMessages] = useState([])

  // =======================================================
  // État du champ input utilisateur
  // =======================================================
  //
  // query :
  // → texte actuellement écrit dans l'input
  //
  // setQuery :
  // → modifie le contenu du champ
  //
  // =======================================================

  const [query, setQuery] = useState("")


  // =======================================================
  // Fonction appelée lors de l'envoi d'un message
  // =======================================================
  //
  // Cette fonction :
  //
  // 1. ajoute le message utilisateur
  // 2. envoie la conversation au backend
  // 3. récupère la réponse IA
  // 4. ajoute la réponse à l'interface
  //
  // =======================================================

  async function handleSend() {

    // =====================================================
    // Création du nouveau tableau de messages
    // =====================================================
    //
    // ...messages :
    // → copie les anciens messages
    //
    // Puis :
    // → ajoute le nouveau message utilisateur
    //
    // =====================================================

    const newMessages = [

      ...messages,

      {
        role: "user",
        content: query
      }
    ]



    // =====================================================
    // Mise à jour immédiate de l'interface
    // =====================================================
    //
    // Le message utilisateur apparaît directement
    // dans le chat avant même la réponse IA.
    //
    // =====================================================

    setMessages(newMessages)



    // =====================================================
    // Envoi de la requête HTTP au backend FastAPI
    // =====================================================
    //
    // axios.post(url, data)
    //
    // URL :
    //
    // http://localhost:8000/chat
    //
    // Données envoyées :
    //
    // {
    //   messages: [...]
    // }
    //
    // =====================================================

    const response = await axios.post(

      "http://localhost:8000/chat",

      {
        messages: newMessages
      }
    )



    // =====================================================
    // Ajout de la réponse IA dans la conversation
    // =====================================================
    //
    // response.data.reply :
    // → réponse retournée par FastAPI
    //
    // Exemple :
    //
    // {
    //   "reply": "Bonjour humain."
    // }
    //
    // =====================================================

    setMessages([

      ...newMessages,

      {
        role: "assistant",
        content: response.data.reply
      }
    ])



    // =====================================================
    // Réinitialisation du champ texte
    // =====================================================
    //
    // Vide l'input après envoi du message.
    //
    // =====================================================

    setQuery("")
  }



  // =======================================================
  // Rendu HTML du composant React
  // =======================================================
  //
  // return() contient toute l'interface utilisateur.
  //
  // =======================================================

  return (

    <div>


      {/* ==================================================
          Titre du chatbot
         ================================================== */}

      <h1>ChatBot</h1>



      {/* ==================================================
          Affichage des messages
         ==================================================
         
         messages.map(...)
         
         Parcourt tous les messages de conversation.
         
         Chaque message affiche :
         
         - le rôle
         - le contenu
         
         ================================================== */}

      {messages.map((msg, i) => (

        <div key={i}>

          <b>{msg.role}</b>: {msg.content}

        </div>
      ))}



      {/* ==================================================
          Champ de saisie utilisateur
         ==================================================
         
         value :
         → valeur actuelle de l'input
         
         onChange :
         → met à jour query à chaque frappe clavier
         
         ================================================== */}

      <input

        value={query}

        onChange={(e) => setQuery(e.target.value)}

      />



      {/* ==================================================
          Bouton d'envoi
         ==================================================
         
         onClick :
         → déclenche handleSend()
         
         ================================================== */}

      <button onClick={handleSend}>

        Envoyer

      </button>

    </div>
  )
}

// =========================================================
// Export du composant
// =========================================================
//
// Permet à React/Vite d'utiliser ce composant
// comme point d'entrée principal de l'application.
//
// =========================================================

export default App
```

### Version plus avancée :

```jsx
import { useState, useRef, useEffect } from 'react'
import axios from "axios"

function App() {

  // =========================================================
  // États
  // =========================================================

  // Historique des messages affichés dans le chat
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Bonjour, comment puis-je vous aider ?" }
  ])

  // Contenu de l'input utilisateur
  const [query, setQuery] = useState("")

  // Vrai pendant qu'on attend la réponse d'Ollama
  const [isLoading, setIsLoading] = useState(false)

  // Référence vers le bas de la liste de messages (pour le scroll auto)
  const bottomRef = useRef(null)


  // =========================================================
  // Scroll automatique vers le dernier message
  // =========================================================

  // S'exécute à chaque fois que `messages` change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])


  // =========================================================
  // Envoi d'un message
  // =========================================================

  async function handleSend() {

    // Nettoyage de l'input (supprime les espaces en début/fin)
    const trimmed = query.trim()

    // Bloque l'envoi si le message est vide ou si une réponse est déjà en cours
    if (!trimmed || isLoading) return

    // Ajout du message utilisateur à l'historique local
    const newMessages = [...messages, { role: "user", content: trimmed }]
    setMessages(newMessages)

    // Réinitialise l'input immédiatement (ne pas attendre la réponse)
    setQuery("")

    // Active l'indicateur de chargement
    setIsLoading(true)

    try {

      // Envoi de l'historique complet au backend FastAPI
      const response = await axios.post("http://localhost:8000/chat", {
        messages: newMessages
      })

      // Ajout de la réponse de l'assistant à l'historique
      setMessages([...newMessages, { role: "assistant", content: response.data.reply }])

    } catch (err) {

      // En cas d'erreur réseau ou serveur, on affiche un message d'erreur
      console.error("Erreur:", err)
      setMessages([...newMessages, { role: "assistant", content: "⚠️ Erreur de connexion." }])

    } finally {

      // Désactive le chargement dans tous les cas (succès ou erreur)
      setIsLoading(false)

    }
  }


  // =========================================================
  // Rendu
  // =========================================================

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-white">

      {/* Barre du haut avec le nom et le statut */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-200 dark:border-gray-800">
        <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-300 text-sm">
          🤖
        </div>
        <span className="text-sm font-medium">Assistant</span>

        {/* Point vert = connecté */}
        <span className="ml-auto text-xs text-gray-400 flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 inline-block" />
          En ligne
        </span>
      </div>

      {/* Zone de messages avec scroll */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
        {messages.map((msg, i) => (

          // Aligne à droite pour l'utilisateur, à gauche pour l'assistant
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`
              max-w-[72%] px-4 py-2.5 text-sm leading-relaxed
              ${msg.role === "user"
                // Bulle bleue pour l'utilisateur, coin haut-droit aplati
                ? "bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100 rounded-xl rounded-tr-sm"
                // Bulle blanche pour l'assistant, coin haut-gauche aplati
                : "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 rounded-xl rounded-tl-sm"
              }
            `}>
              {msg.content}
            </div>
          </div>
        ))}

        {/* Indicateur "en train d'écrire..." affiché pendant le chargement */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl rounded-tl-sm px-4 py-3 flex gap-1">
              {/* 3 points qui pulsent avec un délai décalé */}
              {[0, 1, 2].map(i => (
                <span key={i} className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-pulse"
                  style={{ animationDelay: `${i * 0.15}s` }} />
              ))}
            </div>
          </div>
        )}

        {/* Ancre invisible en bas pour le scroll automatique */}
        <div ref={bottomRef} />
      </div>

      {/* Zone de saisie */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-800 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          // Envoi avec la touche Entrée
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          // Bloqué pendant le chargement
          disabled={isLoading}
          className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 px-4 py-2 rounded-xl text-sm outline-none focus:border-blue-400 disabled:opacity-50"
          placeholder="Écris un message..."
        />

        {/* Bouton d'envoi, désactivé pendant le chargement */}
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 flex items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800 transition disabled:opacity-50"
        >
          ➤
        </button>
      </div>

    </div>
  )
}

export default App
```


---

# 19. Analyse de sentiment

## sentiment.py

```python
from transformers import pipeline

_sentiment_pipeline = None


def get_pipeline():
    global _sentiment_pipeline

    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis"
        )

    return _sentiment_pipeline


def analyze_sentiment(text: str):

    pipe = get_pipeline()

    return pipe(text)
```

---

# 20. Analyse d'image

## vision.py

```python
from PIL import Image


def analyze_image(path: str):

    image = Image.open(path)

    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode
    }
```

---

# 21. Voice Chat

## voice.py

```python
import pyttsx3

engine = pyttsx3.init()


def speak(text: str):
    engine.say(text)
    engine.runAndWait()
```

---

# 22. Recherche de fichiers

## file_search.py

```python
from pathlib import Path


def search_files(query: str, base_path="."):

    results = []

    for path in Path(base_path).rglob("*"):

        if query.lower() in path.name.lower():
            results.append(str(path))

    return results
```

---

# 23. Architecture multi-bots

## Structure

```txt
bots/
├── file_bot/
├── image_bot/
├── support_bot/
├── notes_bot/
└── assistant_bot/
```

---

# 24. Structure d'un bot

```txt
bots/file_bot/
├── handler.py
├── router.py
├── schemas.py
└── prompt_v1.txt
```

---

# 25. Handler métier

## handler.py

```python
from core.file_search import search_files


def handle(query: str):

    files = search_files(query)

    return {
        "reply": f"{len(files)} fichiers trouvés",
        "files": files
    }
```

---

# 26. Router FastAPI

## router.py

```python
from fastapi import APIRouter
from .handler import handle

router = APIRouter()


@router.post("/chat")
def chat(data: dict):

    query = data["query"]

    return handle(query)
```

---

# 27. Brancher les bots

## main.py

```python
from bots.file_bot.router import router as file_router

app.include_router(file_router)
```

---

# 28. Ajouter OpenAI

## Exemple

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
```

---

# 29. Ajouter Mistral

## Exemple

```python
from mistralai.client import MistralClient

client = MistralClient(
    api_key=os.getenv("MISTRAL_API_KEY")
)
```

---

# 30. Ajouter Tauri (desktop)

## Installation

```bash
npm install --save-dev @tauri-apps/cli
```

---

## Initialisation

```bash
npx tauri init
```

---

# 31. Ajouter Docker

## Dockerfile backend

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 32. Docker Compose

```yaml
version: '3'

services:

  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
```

---

# 33. Bonnes pratiques importantes

## Séparer :

* Core réutilisable
* Logique métier
* UI
* Prompts
* Providers LLM

---

## Toujours prévoir :

* fallback local
* mode demo
* logs
* timeout
* blacklist
* gestion erreurs

---

## Versionner les prompts

Exemple :

```txt
prompt_v1.txt
prompt_v1.1.txt
prompt_v2.txt
```

---

# 34. Features bonus avancées

## Suggestions automatiques

Le bot peut proposer :

* commandes rapides
* actions
* boutons contextuels
* suggestions IA

---

## Mémoire conversationnelle

Ajouter :

* historique
* résumé de conversation
* mémoire persistante

---

## RAG local

Ajouter :

* ChromaDB
* FAISS
* embeddings
* PDF parsing

---

## Multi-agent

Exemple :

* agent vision
* agent code
* agent recherche
* agent assistant

---

# 35. Roadmap idéale

## Niveau 1

* Chat simple
* Ollama
* React
* FastAPI

---

## Niveau 2

* Multi-provider
* Prompts versionnés
* Bots modulaires

---

## Niveau 3

* Vision
* Voice
* Sentiment
* Suggestions

---

## Niveau 4

* RAG
* Mémoire
* Multi-agent
* Docker
* Tauri

---

# 36. Architecture finale recommandée

```txt
Frontend React/Tauri
        ↓
FastAPI API Layer
        ↓
Chat Engine
        ↓
LLM Provider Layer
        ↓
Ollama / OpenAI / Mistral
        ↓
Services IA
(vision, voice, sentiment, rag)
        ↓
Handlers métiers
        ↓
Données
(files, DB, APIs)
```

---

# 37. Conseils de développement

## Commencer petit

Ne fais pas tout d'un coup.

Ordre recommandé :

1. Chat simple
2. Ollama
3. Frontend
4. Multi-provider
5. File search
6. Vision
7. Voice
8. RAG
9. Multi-bots

---

## Toujours tester les modules séparément

Exemple :

* tester Ollama seul
* tester FastAPI seul
* tester React seul
* tester vision seule

---

## Créer un vrai socle réutilisable

Ton objectif n'est pas :

❌ créer un seul chatbot

Ton objectif est :

✅ créer un framework de chatbots réutilisable

---

# 38. Conclusion

Avec cette architecture tu peux créer :

* assistant local
* moteur de recherche fichiers
* assistant vocal
* chatbot SAV
* chatbot e-commerce
* assistant code
* assistant notes
* IA desktop
* IA web
* IA multimodale

Le plus important :

* modularité
* séparation des responsabilités
* abstraction des providers
* prompts versionnés
* architecture scalable
---

Je t’ai préparé un guide complet structuré comme un vrai cours de développement pour créer un bundle de chatbots modulaires avec :

* FastAPI
* React + Vite
* Ollama
* Switch OpenAI / Mistral
* Analyse d’image
* Voice chat
* Recherche de fichiers
* Architecture multi-bots
* Core réutilisable
* Docker
* Tauri
* Prompt management
* Vision / sentiment / suggestions

Le guide est pensé comme une base de framework réutilisable, inspirée directement des patterns communs de tes projets C3PO et Bon Vivant.

# ERREURS :

## Pas de retour Ollama :

Le serveur doit être ouvert `ollama serve`
le modèle doit être chargé : `ollama pull llama3`
Test dans la console à la racine du projet :

Test Ollama :
`Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -ContentType "application/json" -Body '{"model":"llama3","prompt":"dis bonjour","stream":false}'`

Test FastAPI :
`Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body '{"messages":[{"role":"user","content":"bonjour"}]}'`

Ca dira exactement où ça coince.

## Pour voir si l'api fonctionne bien :

Se rendre sur http://localhost:8000
Si on a quelque chose comme ça, c'est que c'est bon :

```json
{
"message": "API chatbot OK"
}
```

