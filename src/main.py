from langfuse import get_client
from langfuse.langchain import CallbackHandler
from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Initialize Langfuse client
langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Initialize Langfuse CallbackHandler for LangChain (tracing)
langfuse_handler = CallbackHandler()


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
    return agent.with_config(config={"callbacks": [langfuse_handler]})
