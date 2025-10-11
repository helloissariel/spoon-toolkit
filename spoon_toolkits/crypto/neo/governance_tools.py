"""Governance and Committee Tools for Neo Blockchain"""

from spoon_ai.tools.base import BaseTool, ToolResult
from .base import get_provider


class GetCommitteeInfoTool(BaseTool):
    name: str = "get_committee_info"
    description: str = "Get detailed committee information for Neo blockchain governance. Useful when you need to understand governance structure or analyze committee composition and roles. Returns committee information."
    parameters: dict = {
        "type": "object",
        "properties": {
            "limit":{
                "type": "int",
                "description": "the number of items to return",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            },
            "network": {
                "type": "string",
                "description": "Neo network type, must be 'mainnet' or 'testnet'",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            }
        },
        "required": ["limit"]
    }

    async def execute(self, limit:int,network: str = "testnet") -> ToolResult:
        try:
            async with get_provider(network) as provider:
                response = await provider._make_request("GetCommittee", {Limit:limit})
                result = provider._handle_response(response)
                return ToolResult(output=f"Committee info: {result}")
        except Exception as e:
            return ToolResult(error=str(e)) 