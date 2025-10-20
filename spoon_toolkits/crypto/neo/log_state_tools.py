"""Application Log and State Tools for Neo Blockchain"""

from spoon_ai.tools.base import BaseTool, ToolResult
from .base import get_provider


class GetApplicationLogTool(BaseTool):
    name: str = "get_application_log"
    description: str = "Get application execution logs for Neo blockchain transactions. Useful when you need to analyze smart contract execution logs or debug contract interactions. Returns application log information."
    parameters: dict = {
        "type": "object",
        "properties": {
            "transaction_hash": {
                "type": "string",
                "description": "Transaction hash, must be valid hexadecimal format (e.g., 0x1234567890abcdef)"
            },
            "network": {
                "type": "string",
                "description": "Neo network type, must be 'mainnet' or 'testnet'",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            }
        },
        "required": ["transaction_hash"]
    }

    async def execute(self, transaction_hash: str, network: str = "testnet") -> ToolResult:
        try:
            async with get_provider(network) as provider:
                response = await provider._make_request("GetApplicationLogByTransactionHash", {
                    "TransactionHash": transaction_hash
                })
                result = provider._handle_response(response)
                return ToolResult(output=f"Application log: {result}")
        except Exception as e:
            return ToolResult(error=str(e))


class GetApplicationStateTool(BaseTool):
    name: str = "get_application_state"
    description: str = "Gets the applicationlog by blockhash."
    parameters: dict = {
        "type": "object",
        "properties": {
            "block_hash": {
                "type": "string",
                "description": "blockhash of a transaction, must be valid hexadecimal format (e.g., 0x1234567890abcdef)"
            },
            "network": {
                "type": "string",
                "description": "Neo network type, must be 'mainnet' or 'testnet'",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            },
            "Skip": {
                "type": "integer",
                "description": "the number of items to skip"
            },
            "Limit": {
                "type": "integer",
                "description": "the number of items to return"
            }
        },
        "required": ["block_hash"]
    }

    async def execute(self, block_hash: str, network: str = "testnet", Skip: int = None, Limit: int = None) -> ToolResult:
        try:
            async with get_provider(network) as provider:
                # Build request parameters
                request_params = {"BlockHash": block_hash}

                # Add optional parameters if provided
                if Skip is not None:
                    request_params["Skip"] = Skip
                if Limit is not None:
                    request_params["Limit"] = Limit

                response = await provider._make_request("GetApplicationLogByBlockHash", request_params)
                result = provider._handle_response(response)
                return ToolResult(output=f"Application state: {result}")
        except Exception as e:
            return ToolResult(error=str(e)) 