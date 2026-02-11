from langfuse import get_client
from langfuse.langchain import CallbackHandler
from deepagents import create_deep_agent
from langgraph.graph.state import RunnableConfig

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
        model="azure_openai:gpt-4o-mini-2024-07-18",
        subagents=[reddit_researcher],
        system_prompt="INSTRUCTIONS: Don't use the general-purpose subagent for research!",
    )
    config: RunnableConfig = {"callbacks": [langfuse_handler], "recursion_limit": 50}
    return agent.with_config(config=config)


# TODO: Remove general-purpose.
# TODO: Add Reddit subagent with same middlewares!
