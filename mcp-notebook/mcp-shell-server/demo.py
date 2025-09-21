#!/usr/bin/env python3
"""
Demo script showing how to use the FastMCP Terminal Server

This script demonstrates the basic functionality of the terminal server
by simulating FastMCP client interactions.
"""

import asyncio
import subprocess
import sys
from typing import Dict, Any


def simulate_fastmcp_request(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Simulate a FastMCP request by calling the server directly."""
    # This is a simplified simulation - in reality, you'd use proper FastMCP client libraries
    if tool_name == "terminal":
        command = arguments.get("command", "")
        if not command:
            return "Error: No command provided"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                capture_output=True,
                timeout=30
            )
            return result.stdout or "(No output)"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 30 seconds"
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed with exit code {e.returncode}"
            if e.stderr:
                error_msg += f"\nError output: {e.stderr}"
            return error_msg
        except Exception as e:
            return f"Error executing command: {str(e)}"
    else:
        return f"Unknown tool: {tool_name}"


def main():
    """Run the demo."""
    print("FastMCP Terminal Server Demo")
    print("=" * 40)
    print()
    
    # Demo commands
    demo_commands = [
        "echo 'Hello from FastMCP Terminal Server!'",
        "python --version",
        "dir" if sys.platform == "win32" else "ls -la",
        "echo 'Current directory:' && pwd" if sys.platform != "win32" else "echo Current directory: && cd",
    ]
    
    for i, cmd in enumerate(demo_commands, 1):
        print(f"Demo {i}: {cmd}")
        print("-" * 30)
        
        # Simulate FastMCP tool call
        result = simulate_fastmcp_request("terminal", {"command": cmd})
        print(result)
        print()
    
    print("Demo completed!")
    print()
    print("To use the actual FastMCP server:")
    print("1. Run: python server.py")
    print("2. Connect with a FastMCP client")
    print("3. Call the 'terminal' tool with your commands")


if __name__ == "__main__":
    main()
