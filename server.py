import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def root():
    return {"status": "ok", "message": "MCP backend running"}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    while True:
        prompt = await websocket.receive_text()

        async for event in agent.run_stream(prompt):
            await websocket.send_json(event)
