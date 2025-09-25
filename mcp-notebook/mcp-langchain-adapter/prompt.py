from fastmcp import FastMCP

mcp = FastMCP("research-agent")

@mcp.prompt()
def get_research_prompt(topic: str) -> str:
    return f"Research the topic of {topic}"

if __name__ == "__main__":
    #mcp.run(transport="http")
    mcp.run()
    