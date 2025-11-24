import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

def create_agent():
    load_dotenv()

    config = {
        "mcpServers": {
            "slack": {
                "command": "python",
                "args": ["agent/slack_mcp_server.py"],
                "env": {
                    "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
                    "SLACK_CHANNEL_ID": os.getenv("SLACK_CHANNEL_ID")
                }
            },
            "postgres": {
                "command": "python",
                "args": ["agent/postgres_mcp_server.py"],
                "env": {
                    "SUPABASE_DB_URL": os.getenv("SUPABASE_DB_URL")
                }
            }
        }
    }

    client = MCPClient.from_dict(config)
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    agent = MCPAgent(llm=llm, client=client, max_steps=25)
    return agent
