import os
import httpx
from fastmcp import FastMCP

server = FastMCP("slack-server")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

@server.tool()
async def send_message(message: str):
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
    payload = {"channel": SLACK_CHANNEL_ID, "text": message}
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    return resp.json()

if __name__ == "__main__":
    server.run(transport="stdio")
