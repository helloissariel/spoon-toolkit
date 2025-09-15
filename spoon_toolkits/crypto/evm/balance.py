import os
import logging
from typing import Optional

from pydantic import Field

from spoon_ai.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
]


class EvmBalanceTool(BaseTool):
    name: str = "evm_get_balance"
    description: str = "Get native or ERC20 balance for an address."
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {"type": "string", "description": "RPC endpoint. Defaults to EVM_PROVIDER_URL/RPC_URL env."},
            "address": {"type": "string", "description": "Address to query"},
            "token_address": {"type": "string", "description": "Optional ERC20 token address; if omitted, returns native balance"},
        },
        "required": ["address"],
    }

    rpc_url: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    token_address: Optional[str] = Field(default=None)

    async def execute(self, rpc_url: Optional[str] = None, address: Optional[str] = None, token_address: Optional[str] = None) -> ToolResult:
        try:
            rpc_url = rpc_url or self.rpc_url or os.getenv("EVM_PROVIDER_URL") or os.getenv("RPC_URL")
            address = address or self.address
            token_address = token_address or self.token_address
            if not rpc_url:
                return ToolResult(error="Missing rpc_url and no EVM_PROVIDER_URL/RPC_URL set")
            if not address or not address.startswith("0x"):
                return ToolResult(error="Missing or invalid address")

            try:
                from web3 import Web3, HTTPProvider
            except Exception as e:
                return ToolResult(error=f"web3 dependency not available: {str(e)}")

            w3 = Web3(HTTPProvider(rpc_url))
            if not w3.is_connected():
                return ToolResult(error=f"Failed to connect to RPC: {rpc_url}")

            if token_address:
                token = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
                decimals = int(token.functions.decimals().call())
                bal = token.functions.balanceOf(Web3.to_checksum_address(address)).call()
                value = float(bal) / (10 ** decimals)
                return ToolResult(output={"address": address, "token": Web3.to_checksum_address(token_address), "balance": value})
            else:
                wei = w3.eth.get_balance(Web3.to_checksum_address(address))
                eth = float(wei) / (10 ** 18)
                return ToolResult(output={"address": address, "balance": eth})
        except Exception as e:
            logger.error(f"EvmBalanceTool error: {e}")
            return ToolResult(error=f"Get balance failed: {str(e)}")


