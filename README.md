# 🚀 MCP Agent — Slack + Postgres + FastAPI (WebSocket)

Este proyecto ejecuta un **agente MCP** que puede:

* Consultar **Postgres**
* Enviar mensajes a **Slack**
* Ejecutar acciones con herramientas MCP
* Responder vía **WebSocket** con reasoning paso a paso

Todo corre dentro de **Docker**.

---

# ⚙️ Requisitos

* Docker
* Docker Compose
* Archivo `.env` en la raíz

---

# 📄 Archivo `.env` requerido

```
OPENAI_API_KEY=your_key
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=C123456
SUPABASE_DB_URL=postgresql://user:pass@host:5432/db
```

---

# 🚀 Instalación y ejecución (Docker)

1. Clona el repo
2. Crea tu `.env` con las variables anteriores
3. Ejecuta:

```
docker compose down
docker compose build --no-cache
docker compose up

docker compose up --build
```

Listo.
El backend se levanta automáticamente con:

### 🔌 WebSocket

```
ws://localhost:8000/chat
```

---

# 💬 Cómo usar el WebSocket

Conéctate vía cualquier cliente WS (frontend, wscat, Postman, etc.)

### **Enviar un mensaje**

```
"Consulta los últimos 5 logs desde Postgres."
```

### **Recibirás eventos como:**

Reasoning:

```json
{"type": "thought", "content": "Consultando logs..."}
```

Tool call:

```json
{"type": "tool_call", "tool": "postgres.get_logs"}
```

Resultado final:

```json
{"type": "final", "output": "Logs enviados a Slack."}
```

---

# 📦 Estructura principal del proyecto

```
mcp/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── server.py                    # FastAPI + WebSocket
└── agent/
    ├── agent.py                 # create_agent()
    ├── slack_mcp_server.py
    └── postgres_mcp_server.py
```

---

# 🧪 Probar sin frontend

Instala `wscat`:

```
npm i -g wscat
```

Conéctate:

```
wscat -c ws://localhost:8000/chat
```

---

# 🎉 Listo

Tu agente MCP ya está funcionando en Docker, con comunicación en tiempo real vía WebSocket.

