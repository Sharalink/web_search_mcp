#!/bin/bash
# Enhanced MCP Server startup script
# Created by Emink for enhanced functionality
cd "$(dirname "$0")"
exec uv run python enhanced_server_pure.py
