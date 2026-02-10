from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents import create_deep_agent, CompiledSubAgent
from langchain.agents import create_agent

REDDIT_RESEARCH_INSTRUCTIONS = """
You are a researcher focusing on Reddit communities. Research the topic provided to you.

Minimize your scope to the following subreddits:

<SUBREDDITS>
r/AIAgentsInAction
r/AIMemory
r/AgentsOfAI
r/Anthropic
r/ClaudeAI
r/GeminiAI
r/GithubCopilot
r/HowToAIAgent
r/LLMDevs
r/LLMeng
r/LangChain
r/LargeLanguageModels
r/LlamaFarm
r/LocalLLaMA
r/OpenAI
r/OpenSourceAI
r/PromptEngineering
r/Rag
r/aipromptprogramming
r/cursor
r/dataengineering
r/kimi
r/learnmachinelearning
r/mcp
r/neuralnetworks
r/nvidia
r/opencodeCLI
r/unsloth
</SUBREDDITS>

"""


async def make_reddit_research_subagent():
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
    # Create a custom agent graph
    custom_graph = create_agent(
        model="azure_openai:gpt-4o-mini-2024-07-18",
        tools=tools,
        system_prompt=REDDIT_RESEARCH_INSTRUCTIONS,
    )

    # Use it as a custom subagent
    custom_subagent = CompiledSubAgent(
        name="reddit-research-agent",
        description="Used to look for hot topics on Reddit",
        runnable=custom_graph,
    )
    return custom_subagent
