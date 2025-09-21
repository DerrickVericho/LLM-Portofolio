# FastMCP Terminal Server

A modern Model Context Protocol (MCP) server built with FastMCP that exposes a terminal tool, allowing users to execute shell commands through the MCP interface.

## Features

- **FastMCP Framework**: Built with the modern FastMCP Python SDK
- **Terminal Tool**: Execute shell commands and receive output
- **Enhanced Logging**: Built-in logging and error reporting via FastMCP Context
- **Error Handling**: Proper error handling with timeout protection
- **Security**: 30-second timeout to prevent long-running commands
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. Install dependencies:
```bash
uv sync
```

Or with pip:
```bash
pip install fastmcp
```

## Usage

### Running the Server

Start the FastMCP server:
```bash
python server.py
```

The server will run using FastMCP's built-in transport and wait for MCP client connections.

### Using the Terminal Tool

The server exposes a single tool called `terminal` that accepts a `command` parameter:

```python
from fastmcp import Client

async with Client("python server.py") as client:
    result = await client.call_tool("terminal", {"command": "echo 'Hello World'"})
    print(result)
```

### Example Commands

- `echo "Hello from FastMCP!"`
- `ls -la` (Unix/Linux/macOS) or `dir` (Windows)
- `python --version`
- `pwd` (Unix/Linux/macOS) or `cd` (Windows)

## Testing

Run the test client to verify the server works:

```bash
python test_client.py
```

Or run the demo to see the functionality:

```bash
python demo.py
```

## Security Considerations

⚠️ **WARNING**: This server allows execution of arbitrary shell commands, which can be a significant security risk. Use with caution and consider:

- Running in a sandboxed environment
- Implementing command whitelisting
- Adding user authentication
- Monitoring command execution logs

## Architecture

The server is built using FastMCP and follows these key components:

- `FastMCP`: Modern MCP server framework
- `@mcp.tool`: Decorator for registering tools
- `Context`: FastMCP context for logging and error handling
- Built-in transport: FastMCP handles communication automatically

## Error Handling

The server includes comprehensive error handling:

- **Timeout**: Commands are limited to 30 seconds
- **Process Errors**: Captures and returns stderr output
- **Validation**: Ensures commands are provided
- **Logging**: Uses FastMCP Context for structured logging
- **Exceptions**: Handles unexpected errors gracefully

## FastMCP Benefits

- **Simplified API**: Cleaner, more Pythonic interface
- **Built-in Logging**: Context-based logging and error reporting
- **Modern Framework**: Latest MCP standards and best practices
- **Better Performance**: Optimized for modern Python async/await patterns
