
# Schemas Pydantic utilises par l'API.

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