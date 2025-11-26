import asyncio
import re
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel

from agent.agent import create_agent

agent = create_agent()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ---------- MODELO PARA EL REST ----------
class ChatRequest(BaseModel):
    prompt: str

# ---------- HEALTH ----------
@app.get("/")
def root():
    return {"status": "ok", "message": "MCP backend running"}

# ---------- REST /chat ----------
@app.post("/chat")
async def chat_rest(body: ChatRequest):
    result = await agent.run(body.prompt)
    return {"result": result}


# ---------- WEBSOCKET /chat (streaming) ----------
@app.websocket("/ws")
async def chat_stream(websocket: WebSocket):
    await websocket.accept()

    while True:
        prompt = await websocket.receive_text()

        async for event in agent.stream(prompt):
            await websocket.send_json(event)


# ---------- SSE /chat (estilo ChatGPT) ----------
@app.get("/sse")
async def chat_sse(prompt: str):

    TOOL_HUMAN_NAMES = {
        "send_message": "Enviando la información a Slack…",
        "query": "Consultando los datos…"
    }

    async def event_generator():

        async for raw in agent.stream(prompt):

            # ----- 1. Mensaje final -----
            if isinstance(raw, str):
                yield f"data: {json.dumps({'type': 'final', 'text': raw}, ensure_ascii=False)}\n\n"
                continue

            # ----- 2. Acción + Resultado -----
            if isinstance(raw, tuple):
                action, result = raw

                # ---- Inicio de acción (humanizado estilo ChatGPT) ----
                if hasattr(action, "tool"):
                    human_msg = TOOL_HUMAN_NAMES.get(
                        action.tool,
                        "Estoy trabajando en ello…"
                    )
                    yield f"data: {json.dumps({'type': 'assistant', 'text': human_msg}, ensure_ascii=False)}\n\n"

                # ---- Resultado de la acción (breve, elegante) ----
                #human_msg = "Listo, ya tengo esa parte. Déjame continuar…"
                #yield f"data: {json.dumps({'type': 'assistant', 'text': human_msg}, ensure_ascii=False)}\n\n"

                continue

            # ----- 3. Mensajes normales -----
            if isinstance(raw, dict) and "messages" in raw:
                msg = raw["messages"]
                if isinstance(msg, str):
                    yield f"data: {json.dumps({'type': 'assistant', 'text': msg}, ensure_ascii=False)}\n\n"
                continue

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )