import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

def load_system_prompt():
    with open("agent/system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()
    
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
            "postgres-server": {
                "command": "python",
                "args": ["agent/postgres_mcp_server.py"],
                "env": {
                    "SUPABASE_DB_URL": os.getenv("SUPABASE_DB_URL")
                }
            }
        }
    }
    
    client = MCPClient.from_dict(config)
    system_prompt = load_system_prompt()
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    agent = MCPAgent(llm=llm, client=client, max_steps=25, system_prompt=system_prompt)
    return agent
