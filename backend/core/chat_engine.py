# ChatEngine fait exactement ça :

# il reçoit un message
# il construit un prompt
# il appelle le LLMClient
# il sert de cœur de génération de réponse

from core.llm_client import LLMClient


class ChatEngine:

    def __init__(self):
        self.client = LLMClient()

    def chat(self, message: str):

        prompt = f"""
        User: {message}
        Assistant:
        """

        return self.client.ask(prompt)