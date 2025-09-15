import os
import asyncio
import logging
from typing import Optional

from pydantic import Field

from spoon_ai.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
]


class EvmErc20TransferTool(BaseTool):
    name: str = "evm_erc20_transfer"
    description: str = "Transfer ERC20 tokens on an EVM chain via web3."
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {"type": "string", "description": "RPC endpoint. Defaults to EVM_PROVIDER_URL/RPC_URL env."},
            "private_key": {"type": "string", "description": "Sender private key (0x-prefixed). Defaults to EVM_PRIVATE_KEY env."},
            "token_address": {"type": "string", "description": "ERC20 token contract address"},
            "to_address": {"type": "string", "description": "Recipient address"},
            "amount": {"type": "string", "description": "Amount in human-readable units"},
            "gas_price_gwei": {"type": "number", "description": "Optional gas price override in gwei"},
        },
        "required": ["token_address", "to_address", "amount"],
    }

    rpc_url: Optional[str] = Field(default=None)
    private_key: Optional[str] = Field(default=None)
    token_address: Optional[str] = Field(default=None)
    to_address: Optional[str] = Field(default=None)
    amount: Optional[str] = Field(default=None)
    gas_price_gwei: Optional[float] = Field(default=None)

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None,
        token_address: Optional[str] = None,
        to_address: Optional[str] = None,
        amount: Optional[str] = None,
        gas_price_gwei: Optional[float] = None,
    ) -> ToolResult:
        try:
            rpc_url = rpc_url or self.rpc_url or os.getenv("EVM_PROVIDER_URL") or os.getenv("RPC_URL")
            private_key = private_key or self.private_key or os.getenv("EVM_PRIVATE_KEY")
            token_address = token_address or self.token_address
            to_address = to_address or self.to_address
            amount = amount or self.amount
            gas_price_gwei = gas_price_gwei or self.gas_price_gwei

            if not rpc_url:
                return ToolResult(error="Missing rpc_url and no EVM_PROVIDER_URL/RPC_URL set")
            if not private_key or not private_key.startswith("0x"):
                return ToolResult(error="Missing or invalid private_key; must be 0x-prefixed")
            if not token_address or not token_address.startswith("0x"):
                return ToolResult(error="Missing or invalid token_address")
            if not to_address or not to_address.startswith("0x"):
                return ToolResult(error="Missing or invalid to_address")
            if not amount:
                return ToolResult(error="Missing amount")

            try:
                from web3 import Web3, HTTPProvider
            except Exception as e:
                return ToolResult(error=f"web3 dependency not available: {str(e)}")

            w3 = Web3(HTTPProvider(rpc_url))
            if not w3.is_connected():
                return ToolResult(error=f"Failed to connect to RPC: {rpc_url}")

            account = w3.eth.account.from_key(private_key)
            token = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
            try:
                decimals = int(token.functions.decimals().call())
            except Exception:
                decimals = 18

            amount_raw = int(float(amount) * (10 ** decimals))

            tx = token.functions.transfer(Web3.to_checksum_address(to_address), amount_raw).build_transaction({
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "chainId": w3.eth.chain_id,
            })
            # add gas/gasPrice
            try:
                gas_est = w3.eth.estimate_gas(tx)
                tx["gas"] = int(gas_est * 1.2)
            except Exception:
                tx["gas"] = 120000
            if gas_price_gwei is not None:
                tx["gasPrice"] = w3.to_wei(gas_price_gwei, "gwei")
            else:
                try:
                    tx["gasPrice"] = w3.eth.gas_price
                except Exception:
                    pass

            signed = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

            def wait_receipt():
                return w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

            loop = asyncio.get_event_loop()
            receipt = await loop.run_in_executor(None, wait_receipt)
            if getattr(receipt, "status", 1) == 0:
                return ToolResult(error=f"ERC20 transfer reverted: {tx_hash.hex()}")

            return ToolResult(output={
                "hash": tx_hash.hex(),
                "from": account.address,
                "to": Web3.to_checksum_address(to_address),
                "token": Web3.to_checksum_address(token_address),
                "amount": str(amount),
                "decimals": decimals,
            })
        except Exception as e:
            logger.error(f"EvmErc20TransferTool error: {e}")
            return ToolResult(error=f"ERC20 transfer failed: {str(e)}")


