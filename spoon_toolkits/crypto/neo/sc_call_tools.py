"""Smart Contract Call Tools for Neo Blockchain"""
from spoon_ai.tools.base import BaseTool, ToolResult
from .base import get_provider


class GetScCallByContractHashTool(BaseTool):
    name: str = "get_sccall_by_contracthash"
    description: str = "Gets the ScCall by the contract script hash."
    parameters: dict = {
        "type": "object",
        "properties": {
            "contract_hash": {
                "type": "string",
                "description": "Contract hash, must be valid hexadecimal format (e.g., 0x1234567890abcdef)"
            },
            "network": {
                "type": "string",
                "description": "Neo network type, must be 'mainnet' or 'testnet'",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            }
        },
        "required": ["contract_hash"]
    }

    async def execute(self, contract_hash: str, network: str = "testnet") -> ToolResult:
        try:
            async with get_provider(network) as provider:
                response = await provider._make_request("GetScCallByContractHash", {"ContractHash":contract_hash})
                result = provider._handle_response(response)
                return ToolResult(output=f"GetScCallByContractHash: {result}")
        except Exception as e:
            return ToolResult(error=str(e))

class GetScCallByContractHashAddressTool(BaseTool):
    name: str = "get_sccall_by_contracthash_address"
    description: str = "Gets the ScCall by the contract script hash and user's address."
    parameters: dict = {
        "type": "object",
        "properties": {
            "contract_hash": {
                "type": "string",
                "description": "Contract hash, must be valid hexadecimal format (e.g., 0x1234567890abcdef)"
            },
            "address": {
                "type": "string",
                "description": "the user's address"
            },
            "network": {
                "type": "string",
                "description": "Neo network type, must be 'mainnet' or 'testnet'",
                "enum": ["mainnet", "testnet"],
                "default": "testnet"
            }
        },
        "required": ["contract_hash","address"]
    }

    async def execute(self, contract_hash: str, address:str ,network: str = "testnet") -> ToolResult:
        try:
            async with get_provider(network) as provider:
                response = await provider._make_request("GetScCallByContractHash", {"ContractHash": contract_hash,"Address":address})                
                result = provider._handle_response(response)
                return ToolResult(output=f"GetScCallByContractHashAddress:{result}")
        except Exception as e:
                return ToolResult(error=str(e))
        
class GetScCallByTransactionHashTool(BaseTool):
    name: str = "get_sccall_by_transactionhash"
    description: str = "Gets the ScCall by transaction hash."
    parameters: dict = {
        "type": "object",
        "properties": {
            "transaction_hash": {
                "type": "string",
                "description": "the transaction hash, must be valid hexadecimal format (e.g., 0x1234567890abcdef)"
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
                response = await provider._make_request("GetScCallByTransactionHash", {"TransactionHash": transaction_hash})                
                result = provider._handle_response(response)
                return ToolResult(output=f"GetScCallByTransactionHash:{result}")
        except Exception as e:
                return ToolResult(error=str(e))
        