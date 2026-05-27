# ChatEngine contient le moteur principal du chatbot
from core.llm_client import LLMClient
from core.prompt_manager import load_prompt
class ChatEngine:

    def __init__(self):
        self.client = LLMClient()
        self.system_prompt = load_prompt("exemple_v1.0.txt")
        self.history = []  # historique de la conversation
    def chat(self, message: str):
        # Ajout du message utilisateur à l'historique
        self.history.append(f"User: {message}")
        # Construction du prompt complet
        conversation = "\n".join(self.history)
        prompt = f"{self.system_prompt}\n\n{conversation}\nAssistant:"

        # Appel au LLM
        reply = self.client.ask(prompt)

        # Ajout de la réponse à l'historique
        self.history.append(f"Assistant: {reply}")

        return reply