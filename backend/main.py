from fastapi import FastAPI
from core.chat_engine import ChatEngine
from core.schema import ChatRequest

app = FastAPI()
engine = ChatEngine()


@app.post("/chat")
def chat(req: ChatRequest):

    user_message = req.messages[-1].content

    reply = engine.chat(user_message)

    return {
        "reply": reply
    }