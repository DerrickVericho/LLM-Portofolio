#!/usr/bin/env python3
"""
FastMCP Terminal Server

This server exposes a terminal tool that allows users to execute shell commands
using the modern FastMCP framework. Use with caution as this can be a security risk.
"""

import asyncio
import subprocess
import sys
from typing import Optional

from fastmcp import FastMCP, Context


# Initialize the FastMCP server
mcp = FastMCP(name="terminal-server")


@mcp.tool
async def terminal(command: str, ctx: Context) -> str:
    """
    Execute terminal commands and return the output.
    
    Args:
        command: The shell command to execute
        ctx: FastMCP context for logging and error handling
    
    Returns:
        The command output or error message
    """
    if not command:
        await ctx.error("No command provided")
        return "Error: No command provided"
    
    try:
        # Log the command being executed
        await ctx.log(f"Executing command: {command}")
        
        # Execute the command with timeout
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            timeout=30  # 30 second timeout for safety
        )
        
        output = result.stdout
        if not output:
            output = "(No output)"
            
        await ctx.log(f"Command completed successfully")
        return output
        
    except subprocess.TimeoutExpired:
        error_msg = "Error: Command timed out after 30 seconds"
        await ctx.error(error_msg)
        return error_msg
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed with exit code {e.returncode}"
        if e.stderr:
            error_msg += f"\nError output: {e.stderr}"
        await ctx.error(error_msg)
        return error_msg
        
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        await ctx.error(error_msg)
        return error_msg


def main():
    """Main entry point for the FastMCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
