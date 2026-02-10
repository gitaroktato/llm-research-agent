from langfuse import get_client
from langfuse.langchain import CallbackHandler
from deepagents import create_deep_agent

from src.subagents import make_reddit_research_subagent

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
    reddit_researcher = await make_reddit_research_subagent()
    agent = create_deep_agent(
        model="azure_openai:gpt-4o-mini-2024-07-18", subagents=[reddit_researcher]
    )
    return agent.with_config(config={"callbacks": [langfuse_handler]})
