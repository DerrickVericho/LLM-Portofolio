import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI, OpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

stdio_server = StdioServerParameters(
    command="python",
    args=[r"C:\1. MLDL Project\LLM_Project\mcp-notebook\mcp-langchain-adapter\server\math_server.py"],
)

async def main():
    async with stdio_client(stdio_server) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session initialized")
            
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            
            result = await agent.ainvoke({"messages": HumanMessage(content="What is 5 + 10")})
            print(result["messages"][-1].content)
            

if __name__ == "__main__":
    asyncio.run(main())
