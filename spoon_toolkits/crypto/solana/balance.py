"""Solana balance query tool
This module provides tools for querying SOL and SPL token balances
"""

import logging
from typing import Optional, Dict, Any, List

from pydantic import Field

from spoon_ai.tools.base import BaseTool, ToolResult
from .service import (
    get_rpc_url,
    validate_solana_address,
    lamports_to_sol,
    format_token_amount,
    is_native_sol,
    get_mint_program_id,
    get_associated_token_address_for_program,
    create_request_headers,
    get_api_key,
)
from .constants import ERROR_MESSAGES

logger = logging.getLogger(__name__)


class SolanaBalanceTool(BaseTool):
    """Tool for querying Solana account balances.

    This tool can query both SOL (native) and SPL token balances for any Solana address.
    Supports single address queries and batch queries for multiple addresses.
    """

    name: str = "solana_get_balance"
    description: str = "Get SOL or SPL token balance for Solana addresses"
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {
                "type": "string",
                "description": "Solana RPC endpoint URL. Defaults to SOLANA_RPC_URL env var."
            },
            "address": {
                "type": "string",
                "description": "Solana address to query balance for"
            },
            "addresses": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Multiple Solana addresses for batch query"
            },
            "token_address": {
                "type": "string",
                "description": "SPL token mint address. If omitted, returns SOL balance."
            },
            "include_tokens": {
                "type": "boolean",
                "description": "Include all SPL token balances in response",
                "default": False
            }
        },
        "required": [],
    }

    rpc_url: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    addresses: Optional[List[str]] = Field(default=None)
    token_address: Optional[str] = Field(default=None)
    include_tokens: bool = Field(default=False)

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        address: Optional[str] = None,
        addresses: Optional[List[str]] = None,
        token_address: Optional[str] = None,
        include_tokens: bool = False
    ) -> ToolResult:
        """Execute balance query operation."""
        try:
            # Resolve parameters
            rpc_url = rpc_url or self.rpc_url or get_rpc_url()
            address = address or self.address
            addresses = addresses or self.addresses
            token_address = token_address or self.token_address
            include_tokens = include_tokens if include_tokens is not None else self.include_tokens

            # Validate inputs
            if not address and not addresses:
                return ToolResult(error="Either 'address' or 'addresses' must be provided")

            if address and addresses:
                return ToolResult(error="Cannot specify both 'address' and 'addresses'")

            # Import dependencies
            try:
                from solana.rpc.async_api import AsyncClient
                from solders.pubkey import Pubkey
                from spl.token.client import Token
                from spl.token.constants import TOKEN_PROGRAM_ID
            except ImportError as e:
                return ToolResult(error=f"Solana dependencies not available: {str(e)}")

            # Handle single address query
            if address:
                if not validate_solana_address(address):
                    return ToolResult(error=f"Invalid Solana address: {address}")

                result = await self._query_single_balance(
                    rpc_url, address, token_address, include_tokens
                )
                return result

            # Handle batch addresses query
            else:
                for addr in addresses:
                    if not validate_solana_address(addr):
                        return ToolResult(error=f"Invalid Solana address: {addr}")

                result = await self._query_batch_balances(
                    rpc_url, addresses, token_address, include_tokens
                )
                return result

        except Exception as e:
            logger.error(f"SolanaBalanceTool error: {e}")
            return ToolResult(error=f"Balance query failed: {str(e)}")

    async def _query_single_balance(
        self,
        rpc_url: str,
        address: str,
        token_address: Optional[str],
        include_tokens: bool
    ) -> ToolResult:
        """Query balance for a single address."""
        from solana.rpc.async_api import AsyncClient
        from solders.pubkey import Pubkey

        async with AsyncClient(rpc_url) as client:
            try:
                pubkey = Pubkey.from_string(address)

                # Query SOL balance if no specific token requested
                if not token_address or is_native_sol(token_address):
                    response = await client.get_balance(pubkey)
                    if response.value is None:
                        return ToolResult(error=f"Failed to get balance for {address}")

                    sol_balance = lamports_to_sol(response.value)
                    result = {
                        "address": address,
                        "sol_balance": sol_balance,
                        "lamports": response.value
                    }

                    # Include token balances if requested
                    if include_tokens:
                        token_balances = await self._get_token_balances(client, pubkey)
                        result["token_balances"] = token_balances

                    return ToolResult(output=result)

                # Query specific SPL token balance
                else:
                    if not validate_solana_address(token_address):
                        return ToolResult(error=f"Invalid token address: {token_address}")

                    token_balance = await self._get_spl_token_balance(
                        client, pubkey, token_address
                    )
                    if token_balance is None:
                        return ToolResult(error=f"Failed to get token balance for {token_address}")

                    return ToolResult(output={
                        "address": address,
                        "token_address": token_address,
                        "balance": token_balance["balance"],
                        "ui_amount": token_balance["ui_amount"],
                        "decimals": token_balance["decimals"]
                    })

            except Exception as e:
                logger.error(f"Error querying balance for {address}: {e}")
                raise

    async def _query_batch_balances(
        self,
        rpc_url: str,
        addresses: List[str],
        token_address: Optional[str],
        include_tokens: bool
    ) -> ToolResult:
        """Query balances for multiple addresses."""
        from solana.rpc.async_api import AsyncClient
        from solders.pubkey import Pubkey

        async with AsyncClient(rpc_url) as client:
            try:
                pubkeys = [Pubkey.from_string(addr) for addr in addresses]
                results = {}

                if not token_address or is_native_sol(token_address):
                    # Batch query SOL balances
                    response = await client.get_multiple_accounts(pubkeys)
                    if not response.value:
                        return ToolResult(error="Failed to get account information")

                    for i, (addr, account_info) in enumerate(zip(addresses, response.value)):
                        if account_info:
                            sol_balance = lamports_to_sol(account_info.lamports)
                            results[addr] = {
                                "sol_balance": sol_balance,
                                "lamports": account_info.lamports
                            }

                            if include_tokens:
                                token_balances = await self._get_token_balances(client, pubkeys[i])
                                results[addr]["token_balances"] = token_balances
                        else:
                            results[addr] = {"sol_balance": 0, "lamports": 0}

                else:
                    # Query specific token for all addresses
                    for addr, pubkey in zip(addresses, pubkeys):
                        token_balance = await self._get_spl_token_balance(
                            client, pubkey, token_address
                        )
                        results[addr] = token_balance or {
                            "balance": "0",
                            "ui_amount": 0.0,
                            "decimals": 0
                        }

                return ToolResult(output={
                    "addresses": addresses,
                    "token_address": token_address,
                    "balances": results
                })

            except Exception as e:
                logger.error(f"Error in batch balance query: {e}")
                raise

    async def _get_token_balances(self, client, owner_pubkey) -> List[Dict[str, Any]]:
        """Get all SPL token balances for an address (both legacy and Token-2022)."""
        try:
            from .constants import TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID

            token_balances = []

            # Query both legacy SPL Token and Token-2022 programs
            for program_id in [TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID]:
                try:
                    response = await client.get_token_accounts_by_owner(
                        owner_pubkey,
                        {"programId": program_id},
                        encoding="jsonParsed"
                    )

                    if response.value:
                        for account_info in response.value:
                            try:
                                parsed_data = account_info.account.data.parsed
                                token_info = parsed_data["info"]["tokenAmount"]

                                # Only include accounts with non-zero balance
                                if float(token_info["uiAmount"] or 0) > 0:
                                    token_balances.append({
                                        "mint": parsed_data["info"]["mint"],
                                        "balance": token_info["amount"],
                                        "ui_amount": token_info["uiAmount"],
                                        "decimals": token_info["decimals"],
                                        "program_id": program_id  # Track which program owns this token
                                    })
                            except (KeyError, TypeError) as e:
                                logger.debug(f"Error parsing token account: {e}")
                                continue

                except Exception as e:
                    logger.debug(f"Failed to query {program_id} tokens: {e}")
                    continue

            return token_balances

        except Exception as e:
            logger.error(f"Error getting token balances: {e}")
            return []

    async def _get_spl_token_balance(
        self, client, owner_pubkey, token_mint: str
    ) -> Optional[Dict[str, Any]]:
        """Get SPL token balance for a specific mint (program-aware)."""
        try:
            from solders.pubkey import Pubkey

            # First detect which program owns this mint
            try:
                program_id = await get_mint_program_id(client, token_mint)
            except ValueError as e:
                logger.debug(f"Failed to detect program for mint {token_mint}: {e}")
                # Fall back to legacy program for backward compatibility
                from .constants import TOKEN_PROGRAM_ID
                program_id = TOKEN_PROGRAM_ID

            # Get the correct ATA for this program
            ata_address = get_associated_token_address_for_program(
                str(owner_pubkey), token_mint, program_id
            )
            ata = Pubkey.from_string(ata_address)

            # Get associated token account info
            response = await client.get_account_info(ata, encoding="jsonParsed")

            if not response.value or not response.value.data:
                return {"balance": "0", "ui_amount": 0.0, "decimals": 0, "program_id": program_id}

            parsed_data = response.value.data.parsed
            token_amount = parsed_data["info"]["tokenAmount"]

            return {
                "balance": token_amount["amount"],
                "ui_amount": token_amount["uiAmount"] or 0.0,
                "decimals": token_amount["decimals"],
                "program_id": program_id
            }

        except Exception as e:
            logger.debug(f"Error getting SPL token balance: {e}")
            return None


class SolanaPortfolioTool(BaseTool):
    """Tool for getting comprehensive wallet portfolio information."""

    name: str = "solana_get_portfolio"
    description: str = "Get comprehensive portfolio information for a Solana wallet"
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {
                "type": "string",
                "description": "Solana RPC endpoint URL"
            },
            "address": {
                "type": "string",
                "description": "Solana wallet address"
            },
            "include_prices": {
                "type": "boolean",
                "description": "Include USD prices for tokens",
                "default": True
            }
        },
        "required": ["address"],
    }

    rpc_url: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    include_prices: bool = Field(default=True)

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        address: Optional[str] = None,
        include_prices: bool = True
    ) -> ToolResult:
        """Execute portfolio query operation."""
        try:
            # Resolve parameters
            rpc_url = rpc_url or self.rpc_url or get_rpc_url()
            address = address or self.address
            include_prices = include_prices if include_prices is not None else self.include_prices

            if not address:
                return ToolResult(error="Address is required")

            if not validate_solana_address(address):
                return ToolResult(error=f"Invalid Solana address: {address}")

            # Get basic balance information
            balance_tool = SolanaBalanceTool()
            balance_result = await balance_tool.execute(
                rpc_url=rpc_url,
                address=address,
                include_tokens=True
            )

            if balance_result.error:
                return ToolResult(error=balance_result.error)

            portfolio_data = balance_result.output
            portfolio_data["include_prices"] = include_prices

            # Add price information if requested
            if include_prices:
                try:
                    portfolio_data = await self._add_price_information(portfolio_data)
                except Exception as e:
                    logger.warning(f"Failed to add price information: {e}")
                    portfolio_data["price_warning"] = "Price data unavailable"

            return ToolResult(output=portfolio_data)

        except Exception as e:
            logger.error(f"SolanaPortfolioTool error: {e}")
            return ToolResult(error=f"Portfolio query failed: {str(e)}")

    async def _add_price_information(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add price information to portfolio data."""
        try:
            prices = await fetch_prices_with_cache()
            portfolio_data["prices"] = prices

            # Add USD values if SOL balance exists
            if "sol_balance" in portfolio_data and prices.get("solana", {}).get("usd"):
                sol_price = float(prices["solana"]["usd"])
                sol_balance = portfolio_data["sol_balance"]
                portfolio_data["sol_value_usd"] = sol_balance * sol_price

            # Add price info to token balances if they exist
            if "token_balances" in portfolio_data:
                # For now, only add SOL price info
                # Extended price lookup for individual tokens can be added later
                pass

            logger.info("Price information successfully integrated")
            return portfolio_data
        except Exception as e:
            logger.warning(f"Failed to add price information: {e}")
            portfolio_data["price_error"] = str(e)
            return portfolio_data


# Price caching system

_price_cache = {}
_cache_ttl = 300  # 5 minutes


async def fetch_prices_with_cache(force_refresh: bool = False) -> Dict[str, Dict[str, str]]:
    """Fetch prices for SOL, BTC, ETH with caching support.

    Args:
        force_refresh: Whether to bypass cache and fetch fresh data

    Returns:
        Dictionary with price information for major tokens
    """
    import time
    import httpx
    from .constants import BIRDEYE_API_BASE_URL, TOKEN_ADDRESSES

    cache_key = "prices"
    current_time = time.time()

    # Check cache if not forcing refresh
    if not force_refresh and cache_key in _price_cache:
        cached_data = _price_cache[cache_key]
        if current_time - cached_data["timestamp"] < _cache_ttl:
            logger.debug("Price cache hit")
            return cached_data["data"]

    logger.debug("Price cache miss, fetching fresh data")

    # Default prices structure
    prices = {
        "solana": {"usd": "0"},
        "bitcoin": {"usd": "0"},
        "ethereum": {"usd": "0"},
    }

    try:
        api_key = get_api_key("birdeye")
        if not api_key:
            logger.warning("Birdeye API key not configured, returning default prices")
            return prices

        headers = create_request_headers(api_key)
        token_map = {
            TOKEN_ADDRESSES.get("SOL", "So11111111111111111111111111111111111111112"): "solana",
            TOKEN_ADDRESSES.get("BTC", "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E"): "bitcoin",
            TOKEN_ADDRESSES.get("ETH", "2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk"): "ethereum",
        }

        async with httpx.AsyncClient() as client:
            for token_address, key in token_map.items():
                try:
                    response = await client.get(
                        f"{BIRDEYE_API_BASE_URL}/defi/price",
                        params={"address": token_address},
                        headers=headers,
                        timeout=10
                    )

                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and data.get("data", {}).get("value"):
                            prices[key]["usd"] = str(data["data"]["value"])
                            logger.debug(f"Fetched price for {key}: ${data['data']['value']}")

                except Exception as e:
                    logger.debug(f"Failed to fetch price for {key}: {e}")

        # Cache the results
        _price_cache[cache_key] = {
            "data": prices,
            "timestamp": current_time
        }

        return prices

    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return prices


class SolanaPriceCacheTool(BaseTool):
    """Tool for managing price cache and fetching current token prices."""

    name: str = "solana_price_cache"
    description: str = "Manage price cache and fetch current SOL/BTC/ETH prices"
    parameters: dict = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get", "refresh", "clear", "status"],
                "description": "Price cache operation",
                "default": "get"
            },
            "force_refresh": {
                "type": "boolean",
                "description": "Force refresh cached prices",
                "default": False
            },
            "tokens": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific tokens to get prices for",
                "default": ["SOL", "BTC", "ETH"]
            }
        },
        "required": [],
    }

    action: str = Field(default="get")
    force_refresh: bool = Field(default=False)
    tokens: List[str] = Field(default=["SOL", "BTC", "ETH"])

    async def execute(
        self,
        action: str = "get",
        force_refresh: bool = False,
        tokens: List[str] = ["SOL", "BTC", "ETH"]
    ) -> ToolResult:
        """Execute price cache operation."""
        try:
            action = action or self.action
            force_refresh = force_refresh if force_refresh is not None else self.force_refresh
            tokens = tokens or self.tokens

            if action == "get":
                prices = await fetch_prices_with_cache(force_refresh)

                # Filter to requested tokens
                filtered_prices = {}
                token_mapping = {
                    "SOL": "solana",
                    "BTC": "bitcoin",
                    "ETH": "ethereum"
                }

                for token in tokens:
                    if token in token_mapping:
                        key = token_mapping[token]
                        if key in prices:
                            filtered_prices[token] = prices[key]

                return ToolResult(output={
                    "action": "get",
                    "prices": filtered_prices,
                    "force_refresh": force_refresh,
                    "cache_info": {
                        "cached": not force_refresh and "prices" in _price_cache,
                        "cache_age_seconds": (
                            __import__('time').time() - _price_cache.get("prices", {}).get("timestamp", 0)
                            if "prices" in _price_cache else 0
                        )
                    }
                })

            elif action == "refresh":
                prices = await fetch_prices_with_cache(force_refresh=True)
                return ToolResult(output={
                    "action": "refresh",
                    "prices": prices,
                    "refreshed_at": __import__('time').time(),
                    "status": "success"
                })

            elif action == "clear":
                global _price_cache
                cleared_keys = list(_price_cache.keys())
                _price_cache.clear()

                return ToolResult(output={
                    "action": "clear",
                    "cleared_keys": cleared_keys,
                    "status": "cleared"
                })

            elif action == "status":
                import time
                cache_info = {}

                if "prices" in _price_cache:
                    cached_data = _price_cache["prices"]
                    age = time.time() - cached_data.get("timestamp", 0)
                    cache_info = {
                        "cached": True,
                        "age_seconds": age,
                        "ttl_seconds": _cache_ttl,
                        "expired": age > _cache_ttl,
                        "tokens": list(cached_data.get("data", {}).keys())
                    }
                else:
                    cache_info = {"cached": False}

                return ToolResult(output={
                    "action": "status",
                    "cache_info": cache_info,
                    "cache_ttl": _cache_ttl
                })

            else:
                return ToolResult(error=f"Unknown action: {action}")

        except Exception as e:
            logger.error(f"SolanaPriceCacheTool error: {e}")
            return ToolResult(error=f"Price cache operation failed: {str(e)}")
