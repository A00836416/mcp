import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

async def main():
    load_dotenv()

    # Configuración de tus servidores MCP
    config = {
        "mcpServers": {
            "slack": {
                "command": "python",
                "args": ["slack_mcp_server.py"],
                "env": {
                    "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
                    "SLACK_CHANNEL_ID": os.getenv("SLACK_CHANNEL_ID")
                }
            },
            "postgres": {
                "command": "python",
                "args": ["postgres_mcp_server.py"],
                "env": {
                    "SUPABASE_DB_URL": os.getenv("SUPABASE_DB_URL")
                }
            }
        }
    }

    # Creas el cliente MCP con tu config
    client = MCPClient.from_dict(config)  # según la doc de MCP-use :contentReference[oaicite:0]{index=0}

    llm = ChatOpenAI(model="gpt-4o-mini")

    # Creas el agente MCP-use
    agent = MCPAgent(llm=llm, client=client, max_steps=25)

    # Aquí defines el prompt que vas a ejecutar con tu agente
    result = await agent.run(
        "Consulta los últimos 5 logs desde Postgres y envíalos a Slack."
    )

    print("\nRESULTADO AGENTE:\n", result)

if __name__ == "__main__":
    asyncio.run(main())
