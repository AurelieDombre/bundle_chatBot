# ChatEngine contient le moteur principal du chatbot
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