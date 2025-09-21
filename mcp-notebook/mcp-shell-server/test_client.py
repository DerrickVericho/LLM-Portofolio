#!/usr/bin/env python3
"""
FastMCP test client for the Terminal Server

This script demonstrates how to connect to and use the FastMCP terminal server.
"""

import asyncio
import sys
from fastmcp import Client


async def test_terminal_server():
    """Test the terminal server with a few commands."""
    print("FastMCP Terminal Server Test")
    print("=" * 35)
    
    # Test commands
    test_commands = [
        "echo 'Hello from FastMCP!'",
        "dir" if sys.platform == "win32" else "ls -la",
        "python --version"
    ]
    
    try:
        async with Client("python server.py") as client:
            for cmd in test_commands:
                print(f"\nExecuting: {cmd}")
                print("-" * 25)
                
                try:
                    result = await client.call_tool("terminal", {"command": cmd})
                    print(result)
                except Exception as e:
                    print(f"Error: {e}")
            
            print("\nTest completed!")
            
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        print("Make sure the server is running with: python server.py")


if __name__ == "__main__":
    asyncio.run(test_terminal_server())
