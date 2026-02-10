from langchain_mcp_adapters.sessions import Connection
from langgraph.graph.state import CompiledStateGraph
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient, StdioConnection

from deepagents import create_deep_agent

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "reddit-mcp-buddy"],
)

agent: CompiledStateGraph


async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            agent = create_deep_agent(
                model="azure_openai:gpt-4o-mini-2024-07-18", tools=tools
            )
            return agent


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
