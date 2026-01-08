from fastapi import FastAPI
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat_service

app = FastAPI(title="Persona Chatbot")

@app.post("/chat")
def chat(req: ChatRequest):
    reply = chat_service(req.user_id, req.message)
    return {"reply": reply}
