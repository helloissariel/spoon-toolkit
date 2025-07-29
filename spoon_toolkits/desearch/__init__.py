"""
Desearch AI Integration for Spoon Toolkit

This module provides AI-powered search and metadata extraction capabilities
for the Spoon framework, enabling real-time, verifiable access to open web data.
"""

from fastmcp import FastMCP
from .ai_search import mcp as ai_search_server
from .data_verification import mcp as data_verification_server
from .multi_source_search import mcp as multi_source_search_server

mcp_server = FastMCP("DesearchServer")
mcp_server.mount("AISearch", ai_search_server)
mcp_server.mount("DataVerification", data_verification_server)
mcp_server.mount("MultiSourceSearch", multi_source_search_server)

if __name__ == "__main__":
    mcp_server.run() 