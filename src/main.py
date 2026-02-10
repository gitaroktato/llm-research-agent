from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


async def make_agent():
    client = MultiServerMCPClient(
        {
            "reddit": {
                "command": "npx",
                "args": ["-y", "reddit-mcp-buddy"],
                "transport": "stdio",
            },
        }
    )  # pyright: ignore
    tools = await client.get_tools()
    agent = create_deep_agent(model="azure_openai:gpt-4o-mini-2024-07-18", tools=tools)
    return agent
