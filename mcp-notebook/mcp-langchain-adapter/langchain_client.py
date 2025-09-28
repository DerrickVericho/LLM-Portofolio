import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    r"C:\1. MLDL Project\LLM_Project\mcp-notebook\mcp-langchain-adapter\server\math_server.py"
                ],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    
    async with client.session("math") as session:
        agent = create_react_agent(llm, await client.get_tools())
        result = await agent.ainvoke({"messages": "What is the weather in LA?"})
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
