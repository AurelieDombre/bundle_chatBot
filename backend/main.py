from fastapi import FastAPI
from core.chat_engine import ChatEngine
from core.schema import ChatRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
engine = ChatEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/chat")
def chat(req: ChatRequest):

    user_message = req.messages[-1].content

    reply = engine.chat(user_message)

    return {
        "reply": reply
    }