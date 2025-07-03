#!/usr/bin/env python3
"""
Interactive Feedback MCP Server using native MCP SDK
Developed by Fábio Ferreira (https://x.com/fabiomlferreira)
Inspired by/related to dotcursorrules.com (https://dotcursorrules.com/)
"""

import asyncio
import os
import sys
import json
import tempfile
import subprocess
from typing import Any

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


def launch_feedback_ui(project_directory: str, summary: str) -> dict[str, str]:
    """Launch the feedback UI and return the result"""
    # Create a temporary file for the feedback result
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_file = tmp.name

    try:
        # Get the path to feedback_ui.py relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        feedback_ui_path = os.path.join(script_dir, "feedback_ui.py")

        # Run feedback_ui.py as a separate process
        args = [
            sys.executable,
            "-u",
            feedback_ui_path,
            "--project-directory",
            project_directory,
            "--prompt",
            summary,
            "--output-file",
            output_file,
        ]
        result = subprocess.run(
            args,
            check=False,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True,
        )
        if result.returncode != 0:
            raise Exception(f"Failed to launch feedback UI: {result.returncode}")

        # Read the result from the temporary file
        with open(output_file, "r") as f:
            result = json.load(f)
        os.unlink(output_file)
        return result
    except Exception as e:
        if os.path.exists(output_file):
            os.unlink(output_file)
        raise e


def first_line(text: str) -> str:
    """Get the first line of text, stripped"""
    return text.split("\n")[0].strip()


# Create the server instance
server = Server("Interactive Feedback MCP")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="interactive_feedback",
            description="Request interactive feedback for a given project directory and summary. This tool opens a UI where the user can provide feedback and run commands.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_directory": {
                        "type": "string",
                        "description": "Full path to the project directory",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Short, one-line summary of the changes",
                    },
                },
                "required": ["project_directory", "summary"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """Handle tool calls"""
    if name != "interactive_feedback":
        raise ValueError(f"Unknown tool: {name}")

    project_directory = arguments.get("project_directory", "")
    summary = arguments.get("summary", "")

    try:
        result = launch_feedback_ui(first_line(project_directory), first_line(summary))

        # Format the response
        command_logs = result.get("command_logs", "")
        interactive_feedback = result.get("interactive_feedback", "")

        response = f"Command logs:\n{command_logs}\n\nInteractive feedback:\n{interactive_feedback}"

        return [types.TextContent(type="text", text=response)]
    except Exception as e:
        error_msg = f"Error: {str(e)}\nFailed to launch feedback UI: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point"""
    # Run the server using stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Interactive Feedback MCP",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
