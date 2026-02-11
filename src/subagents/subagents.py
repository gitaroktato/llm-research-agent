from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents import create_deep_agent, CompiledSubAgent
from langchain.agents import create_agent

REDDIT_RESEARCH_INSTRUCTIONS = """
You are a researcher focusing on Reddit communities. Research the topic provided to you.

Minimize your scope to the following subreddits:

<SUBREDDITS>
AIAgentsInAction
AIMemory
AgentsOfAI
Anthropic
ClaudeAI
GeminiAI
GithubCopilot
HowToAIAgent
LLMDevs
LLMeng
LangChain
LargeLanguageModels
LlamaFarm
LocalLLaMA
OpenAI
OpenSourceAI
PromptEngineering
Rag
aipromptprogramming
cursor
dataengineering
kimi
learnmachinelearning
mcp
neuralnetworks
nvidia
opencodeCLI
unsloth
</SUBREDDITS>

"""

REDDIT_RESEARCH_INSTRUCTIONS_SHORT = """
You are a researcher focusing on Reddit communities. Research the topic provided to you.

Minimize your scope to the following subreddits:

<SUBREDDITS>
LocalLLaMA
unsloth
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
        system_prompt=REDDIT_RESEARCH_INSTRUCTIONS_SHORT,
    )

    # Use it as a custom subagent
    custom_subagent = CompiledSubAgent(
        name="reddit-research-agent",
        description="Used to look for hot topics on Reddit",
        runnable=custom_graph,
    )
    return custom_subagent
