# Interactive Feedback MCP (原始版本)

> **原作者：** Fábio Ferreira ([@fabiomlferreira](https://x.com/fabiomlferreira))  
> **项目链接：** [dotcursorrules.com](https://dotcursorrules.com/)

Simple [MCP Server](https://modelcontextprotocol.io/) to enable a human-in-the-loop workflow in AI-assisted development tools like [Cursor](https://www.cursor.com). This server allows you to run commands, view their output, and provide textual feedback directly to the AI. It is also compatible with [Cline](https://cline.bot) and [Windsurf](https://windsurf.com).

## 🚨 Latest Update (Jan 2025) - Cursor Compatibility Fix

Due to recent Cursor updates, some users may experience issues with the MCP server. We've added a **native MCP implementation** that provides better compatibility:

- **Use `server_native.py`** instead of `server.py` if you're experiencing issues
- Supports latest Cursor versions with improved stability
- Maintains all original functionality

## Prompt Engineering

For the best results, add the following to your custom prompt in your AI assistant, you should add it on a rule or directly in the prompt (e.g., Cursor):

> Whenever you want to ask a question, always call the MCP `interactive_feedback`.  
> Whenever you're about to complete a user request, call the MCP `interactive_feedback` instead of simply ending the process.
> Keep calling MCP until the user's feedback is empty, then end the request.

This will ensure your AI assistant uses this MCP server to request user feedback before marking the task as completed.

## 💡 Why Use This?
By guiding the assistant to check in with the user instead of branching out into speculative, high-cost tool calls, this module can drastically reduce the number of premium requests (e.g., OpenAI tool invocations) on platforms like Cursor. In some cases, it helps consolidate what would be up to 25 tool calls into a single, feedback-aware request — saving resources and improving performance.

## Configuration

This MCP server uses Qt's `QSettings` to store configuration on a per-project basis. This includes:
*   The command to run.
*   Whether to execute the command automatically on the next startup for that project (see "Execute automatically on next run" checkbox).
*   The visibility state (shown/hidden) of the command section (this is saved immediately when toggled).
*   Window geometry and state (general UI preferences).

These settings are typically stored in platform-specific locations (e.g., registry on Windows, plist files on macOS, configuration files in `~/.config` or `~/.local/share` on Linux) under an organization name "FabioFerreira" and application name "InteractiveFeedbackMCP", with a unique group for each project directory.

The "Save Configuration" button in the UI primarily saves the current command typed into the command input field and the state of the "Execute automatically on next run" checkbox for the active project. The visibility of the command section is saved automatically when you toggle it. General window size and position are saved when the application closes.

## Installation (Cursor)

1.  **Prerequisites:**
    *   Python 3.11 or newer.
    *   [uv](https://github.com/astral-sh/uv) (Python package manager). Install it with:
        *   Windows: `pip install uv`
        *   Linux/Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2.  **Get the code:**
    *   Clone this repository:
        `git clone https://github.com/noopstudios/interactive-feedback-mcp.git`
    *   Or download the source code.
3.  **Navigate to the directory:**
    *   `cd path/to/interactive-feedback-mcp`
4.  **Install dependencies:**
    *   `uv sync` (this creates a virtual environment and installs packages)
5.  **Run the MCP Server:**
    *   **Recommended (new):** `uv run server_native.py`
    *   **Alternative:** `uv run server.py`
6.  **Configure in Cursor:**
    *   Cursor typically allows specifying custom MCP servers in its settings. You'll need to point Cursor to this running server. The exact mechanism might vary, so consult Cursor's documentation for adding custom MCPs.

## Available tools

Here's an example of how the AI assistant would call the `interactive_feedback` tool:

```xml
<use_mcp_tool>
  <server_name>interactive-feedback-mcp</server_name>
  <tool_name>interactive_feedback</tool_name>
  <arguments>
    {
      "project_directory": "/path/to/your/project",
      "summary": "I've implemented the changes you requested and refactored the main module."
    }
  </arguments>
</use_mcp_tool>
```

## Acknowledgements & Contact

If you find this Interactive Feedback MCP useful, the best way to show appreciation is by following Fábio Ferreira on [X @fabiomlferreira](https://x.com/fabiomlferreira).

For any questions, suggestions, or if you just want to share how you're using it, feel free to reach out on X!

Also, check out [dotcursorrules.com](https://dotcursorrules.com/) for more resources on enhancing your AI-assisted development workflow. 