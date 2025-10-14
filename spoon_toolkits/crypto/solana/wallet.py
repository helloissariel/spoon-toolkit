"""Solana wallet management tools"""
import logging
from typing import Optional, Dict, Any, List
from solders.keypair import Keypair
import base58
import base64
from pydantic import Field
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from spoon_ai.tools.base import BaseTool, ToolResult
from .utils import (
    get_rpc_url, validate_solana_address, validate_private_key,
    get_wallet_keypair, truncate_address
)
from .service import get_wallet_cache_scheduler  

logger = logging.getLogger(__name__)  

class SolanaCreateWalletTool(BaseTool):
    name: str = "solana_create_wallet"
    description: str = "Create a new Solana wallet with keypair"
    parameters: dict = {
        "type": "object",
        "properties": {
            "return_private_key": {
                "type": "boolean",
                "description": "Whether to return the private key in response",
                "default": True
            },
        },
        "required": [],
    }  

    return_private_key: bool = Field(default=True)
    async def execute(self,return_private_key: bool = True) -> ToolResult:
        keypair = Keypair()
        public_key = str(keypair.pubkey())
        result = {"public_key": public_key,"address": public_key,  "truncated_address": truncate_address(public_key)}
        if return_private_key:
            private_key_bytes = bytes(keypair)
            private_key_base58 = base58.b58encode(private_key_bytes).decode('utf-8')
            result["private_key"] = private_key_base58 

        return ToolResult(output=result)  

class SolanaImportWalletTool(BaseTool):
    name: str = "solana_import_wallet"
    description: str = "Import a Solana wallet from private key to validate a user-supplied private key before attaching it to an agent, or to expose an 鈥渋mport wallet鈥� command within the toolkit."
    parameters: dict = {
        "type": "object",
        "properties": {
            "private_key": {
                "type": "string",
                "description": "Private key in base58 or base64 format"
            },
            "validate_only": {
                "type": "boolean",
                "description": "Only validate the private key without importing",
                "default": False
            }
        },
        "required": ["private_key"],
    }  

    private_key: Optional[str] = Field(default=None)
    validate_only: bool = Field(default=False)

    async def execute(self, private_key: Optional[str] = None, validate_only: bool = False) -> ToolResult:
        try:
            private_key = (private_key or self.private_key or "").strip()
            validate_only = validate_only if validate_only is not None else self.validate_only

            if not private_key:
                return ToolResult(error="Private key is required")

            if not validate_private_key(private_key):
                return ToolResult(error="Invalid private key format")

            keypair = None
            decode_errors: List[str] = []

            for fmt, decoder in (
                ("base58", lambda value: base58.b58decode(value)),
                ("base64", lambda value: base64.b64decode(value)),
            ):
                try:
                    secret_key = decoder(private_key)
                    if len(secret_key) != 64:
                        raise ValueError("Invalid key length")
                    keypair = Keypair.from_bytes(secret_key)
                    break
                except Exception as err:
                    decode_errors.append(f"{fmt}: {err}")

            if keypair is None:
                logger.debug("SolanaImportWalletTool decode errors: %s", decode_errors)
                return ToolResult(error="Unable to decode private key")

            public_key = str(keypair.pubkey())
            result = {
                "success": True,
                "public_key": public_key,
                "address": public_key,
                "truncated_address": truncate_address(public_key),
                "validation_status": "valid",
            }

            if not validate_only:
                result["private_key"] = base58.b58encode(bytes(keypair)).decode("utf-8")

            return ToolResult(output=result)

        except Exception as err:
            logger.error(f"SolanaImportWalletTool error: {err}")
            return ToolResult(error="Unable to decode private key")

class SolanaWalletInfoTool(BaseTool):
    name: str = "solana_wallet_info"
    description: str = "Get comprehensive wallet information including balance and tokens"
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {
                "type": "string",
                "description": "Solana RPC endpoint URL"
            },
            "address": {
                "type": "string",
                "description": "Wallet address to query. If omitted, uses configured wallet."
            },
            "include_tokens": {
                "type": "boolean",
                "description": "Include SPL token balances",
                "default": True
            },
            "token_limit": {
                "type": "integer",
                "description": "Maximum number of tokens to include",
                "default": 20
            }
        },
        "required": [],
    }  

    rpc_url: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    include_tokens: bool = Field(default=True)
    token_limit: int = Field(default=20)  

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        address: Optional[str] = None,
        include_tokens: bool = True,
        token_limit: int = 20
    ) -> ToolResult:
        """Execute wallet info query."""
        try:
            # Resolve parameters
            rpc_url = rpc_url or self.rpc_url or get_rpc_url()
            address = address or self.address
            include_tokens = include_tokens if include_tokens is not None else self.include_tokens
            token_limit = token_limit if token_limit is not None else self.token_limit  

            if not address:
                try:
                    keypair_result = get_wallet_keypair(require_private_key=False)
                    if keypair_result.public_key:
                        address = str(keypair_result.public_key)
                    else:
                        return ToolResult(error="No address provided and no wallet configured")
                except Exception:
                    return ToolResult(error="No address provided and no wallet configured")  

            if not validate_solana_address(address):
                return ToolResult(error=f"Invalid wallet address: {address}")  

            scheduler = get_wallet_cache_scheduler()
            await scheduler.ensure_running(rpc_url, address, include_tokens)
            cached = await scheduler.get_cached(rpc_url, address)  

            if cached and cached.get("data"):
                wallet_data = cached["data"]
            else:
                wallet_data = await scheduler.force_refresh(rpc_url, address, include_tokens)
            result = {
                "address": address,
                "truncated_address": truncate_address(address),
                "sol_balance": wallet_data.get("sol_balance", 0),
                "lamports": wallet_data.get("lamports", 0),
                "token_count": 0,
                "tokens": []
            }  

            # Process token balances
            if include_tokens and "token_balances" in wallet_data:
                tokens = wallet_data["token_balances"][:token_limit]
                result["token_count"] = len(wallet_data["token_balances"])
                result["tokens"] = []  

                for token in tokens:
                    result["tokens"].append({
                        "mint": token["mint"],
                        "balance": token["ui_amount"],
                        "decimals": token["decimals"],
                        "raw_balance": token["balance"]
                    })  

            return ToolResult(output=result)  

        except Exception as e:
            logger.error(f"SolanaWalletInfoTool error: {e}")
            return ToolResult(error=f"Wallet info query failed: {str(e)}")  

class SolanaMultiWalletTool(BaseTool):
    """Tool for managing multiple wallets."""
    name: str = "solana_multi_wallet"
    description: str = "Get information for multiple wallets at once"
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {
                "type": "string",
                "description": "Solana RPC endpoint URL"
            },
            "addresses": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of wallet addresses"
            },
            "include_tokens": {
                "type": "boolean",
                "description": "Include token balances for each wallet",
                "default": False
            }
        },
        "required": ["addresses"],
    }  

    rpc_url: Optional[str] = Field(default=None)
    addresses: Optional[List[str]] = Field(default=None)
    include_tokens: bool = Field(default=False)  

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        addresses: Optional[List[str]] = None,
        include_tokens: bool = False
    ) -> ToolResult:
        try:
            rpc_url = rpc_url or self.rpc_url or get_rpc_url()
            addresses = addresses or self.addresses
            include_tokens = include_tokens if include_tokens is not None else self.include_tokens  

            if not addresses:
                return ToolResult(error="Addresses list is required")  

            # Validate all addresses
            for addr in addresses:
                if not validate_solana_address(addr):
                    return ToolResult(error=f"Invalid address: {addr}")  

            # Use batch balance tool
            from .balance import SolanaBalanceTool
            balance_tool = SolanaBalanceTool()  

            batch_result = await balance_tool.execute(
                rpc_url=rpc_url,
                addresses=addresses,
                include_tokens=include_tokens
            )
            if batch_result.error:
                return ToolResult(error=batch_result.error)
            # Format results
            wallet_infos = []
            balances_data = batch_result.output.get("balances", {})  

            for address in addresses:
                balance_info = balances_data.get(address, {})
                wallet_info = {
                    "address": address,
                    "truncated_address": truncate_address(address),
                    "sol_balance": balance_info.get("sol_balance", 0),
                    "lamports": balance_info.get("lamports", 0)
                }  

                if include_tokens and "token_balances" in balance_info:
                    wallet_info["token_count"] = len(balance_info["token_balances"])
                    wallet_info["tokens"] = balance_info["token_balances"]  

                wallet_infos.append(wallet_info)  

            return ToolResult(output={
                "wallet_count": len(addresses),
                "wallets": wallet_infos,
                "total_sol": sum(w["sol_balance"] for w in wallet_infos)
            })  

        except Exception as e:
            logger.error(f"SolanaMultiWalletTool error: {e}")
            return ToolResult(error=f"Multi-wallet query failed: {str(e)}")  

async def get_multiple_wallet_balances(rpc_url: str, addresses: List[str]) -> Dict[str, Dict[str, Any]]:
    """Get SOL balances for multiple wallets ."""
    try:
        from .utils import lamports_to_sol  

        results = {}  

        async with AsyncClient(rpc_url) as client:
            # Convert addresses to pubkeys
            pubkeys = [Pubkey.from_string(addr) for addr in addresses]  

            # Initialize results with default values for all addresses
            for addr in addresses:
                results[addr] = {
                    "sol_balance": 0,
                    "lamports": 0,
                    "exists": False,
                    "error": None
                }
            try:
                # Batch query account info
                response = await client.get_multiple_accounts(pubkeys)  

                if response.value:
                    for i, (addr, account_info) in enumerate(zip(addresses, response.value)):
                        if account_info:
                            sol_balance = lamports_to_sol(account_info.lamports)
                            results[addr] = {
                                "sol_balance": sol_balance,
                                "lamports": account_info.lamports,
                                "exists": True,
                                "error": None
                            }
                else:
                    for addr in addresses:
                        results[addr]["error"] = "RPC returned no data"
            except Exception as e:
                for addr in addresses:
                    results[addr]["error"] = f"RPC error: {str(e)}"
        return results  

    except Exception as e:
        logger.error(f"Error getting multiple wallet balances: {e}")
        return {addr: {"error": str(e)} for addr in addresses}  
