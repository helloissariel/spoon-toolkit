import logging
from typing import Optional, Dict, Any, Union
import httpx
from pydantic import Field
from spoon_ai.tools.base import BaseTool, ToolResult
from .utils import (
    get_rpc_url, get_wallet_key,
    is_native_sol, parse_token_amount, format_token_amount,
    parse_transaction_error
)
from .constants import (
    JUPITER_QUOTE_ENDPOINT, JUPITER_SWAP_ENDPOINT, NATIVE_SOL_ADDRESS,
    MAX_SLIPPAGE_BPS, JUPITER_PRIORITY_LEVELS
)
from solana.rpc.async_api import AsyncClient
logger = logging.getLogger(__name__)

class SolanaSwapTool(BaseTool):

    name: str = "solana_swap"
    description: str = "Swap tokens on Solana using Jupiter aggregator"
    parameters: dict = {
        "type": "object",
        "properties": {
            "rpc_url": {
                "type": "string",
                "description": "Solana RPC endpoint URL. Defaults to SOLANA_RPC_URL env var."
            },
            "private_key": {
                "type": "string",
                "description": "Wallet private key. Defaults to SOLANA_PRIVATE_KEY env var."
            },
            "input_token": {
                "type": "string",
                "description": "Input token mint address (or 'SOL' for native SOL)"
            },
            "output_token": {
                "type": "string",
                "description": "Output token mint address (or 'SOL' for native SOL)"
            },
            "amount": {
                "type": ["string", "number"],
                "description": "Amount to swap (in input token units)"
            },
            "slippage_bps": {
                "type": "integer",
                "description": "Slippage tolerance in basis points (100 = 1%)",
            },
            "priority_level": {
                "type": "string",
                "enum": ["low", "medium", "high", "veryHigh"],
                "description": "Priority level for transaction processing",
                "default": "veryHigh"
            }
        },
        "required": ["input_token", "output_token", "amount"],
    }

    rpc_url: Optional[str] = Field(default=None)
    private_key: Optional[str] = Field(default=None)
    input_token: Optional[str] = Field(default=None)
    output_token: Optional[str] = Field(default=None)
    amount: Optional[Union[str, float]] = Field(default=None)
    slippage_bps: Optional[int] = Field(default=None)
    priority_level: str = Field(default="veryHigh")

    async def execute(
        self,
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None,
        input_token: Optional[str] = None,
        output_token: Optional[str] = None,
        amount: Optional[Union[str, float]] = None,
        slippage_bps: Optional[int] = None,
        priority_level: str = "veryHigh"
    ) -> ToolResult:
        """Execute token swap operation."""
        try:
            # Resolve parameters
            rpc_url = rpc_url or self.rpc_url or get_rpc_url()
            private_key = private_key or self.private_key
            input_token = input_token or self.input_token
            output_token = output_token or self.output_token
            amount = amount or self.amount
            slippage_bps = slippage_bps if slippage_bps is not None else self.slippage_bps
            priority_level = priority_level or self.priority_level

            # Get wallet keypair with dynamic private key support
            keypair_result = get_wallet_key(require_private_key=True, private_key=private_key)
            if not keypair_result.keypair:
                return ToolResult(error="Failed to get wallet keypair")
            wallet_keypair = keypair_result.keypair
            wallet_pubkey = str(wallet_keypair.pubkey())

            # Build quote context (validates inputs and fetches quote)
            quote_context = await self._build_quote_context(
                rpc_url=rpc_url,
                input_token=input_token,
                output_token=output_token,
                amount=amount,
                slippage_bps=slippage_bps,
                user_public_key=wallet_pubkey
            )

            if not quote_context["success"]:
                return ToolResult(error=quote_context["error"])

            quote = quote_context["quote"]

            # Get swap transaction
            swap_result = await self._get_jupiter_swap_transaction(
                quote, wallet_pubkey, priority_level
            )

            if not swap_result["success"]:
                return ToolResult(error=swap_result["error"])

            # Execute swap
            execute_result = await self._execute_swap_transaction(
                rpc_url, wallet_keypair, swap_result["swap_transaction"]
            )

            if not execute_result["success"]:
                return ToolResult(error=execute_result["error"])

            # Format output
            output_amount = quote_context["output_amount"]

            return ToolResult(output={
                "success": True,
                "signature": execute_result["signature"],
                "input_token": input_token,
                "output_token": output_token,
                "input_amount": amount,
                "output_amount": output_amount,
                "price_impact": float(quote.get("priceImpactPct", 0)),
                "slippage_bps": quote_context["slippage_bps"],
                "route_plan": quote.get("routePlan", []),
                "fees": execute_result.get("fees", {})
            })

        except Exception as e:
            logger.error(f"SolanaSwapTool error: {e}")
            return ToolResult(error=f"Swap failed: {str(e)}")

    async def _build_quote_context(
        self,
        rpc_url: str,
        input_token: Optional[str],
        output_token: Optional[str],
        amount: Optional[Union[str, float]],
        slippage_bps: Optional[int],
        user_public_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate inputs, resolve decimals, and fetch a Jupiter quote."""
        if not input_token or not output_token:
            return {"success": False, "error": "Both input_token and output_token are required"}

        if amount is None:
            return {"success": False, "error": "Amount is required"}

        try:
            from decimal import Decimal, InvalidOperation
            amount_decimal = Decimal(str(amount))
        except (TypeError, InvalidOperation):
            return {"success": False, "error": "Invalid amount format"}

        if amount_decimal <= 0:
            return {"success": False, "error": "Amount must be positive"}

        if slippage_bps is not None and (slippage_bps < 1 or slippage_bps > MAX_SLIPPAGE_BPS):
            return {"success": False, "error": f"Slippage must be between 1 and {MAX_SLIPPAGE_BPS} bps"}

        input_mint = self._normalize_token_address(input_token)
        output_mint = self._normalize_token_address(output_token)

        if input_mint == output_mint:
            return {"success": False, "error": "Input and output tokens cannot be the same"}

        input_decimals = await self._get_token_decimals(rpc_url, input_mint)
        if input_decimals is None:
            return {"success": False, "error": f"Failed to get decimals for input token: {input_token}"}

        input_amount_raw = parse_token_amount(str(amount_decimal), input_decimals)

        quote_result = await self._get_jupiter_quote(
            input_mint, output_mint, input_amount_raw, slippage_bps, user_public_key
        )

        if not quote_result["success"]:
            return {"success": False, "error": quote_result["error"]}

        quote = quote_result["quote"]
        output_decimals = await self._get_token_decimals(rpc_url, output_mint)
        if output_decimals is None:
            return {
                "success": False,
                "error": f"Failed to get decimals for output token: {output_token}"
            }

        output_amount = format_token_amount(int(quote["outAmount"]), output_decimals)

        return {
            "success": True,
            "input_mint": input_mint,
            "output_mint": output_mint,
            "input_amount_raw": input_amount_raw,
            "quote": quote,
            "output_decimals": output_decimals,
            "output_amount": output_amount,
            "slippage_bps": slippage_bps,
        }

    def _normalize_token_address(self, token: str) -> str:
        """Normalize token address for Jupiter API."""
        if token.upper() == "SOL" or is_native_sol(token):
            return NATIVE_SOL_ADDRESS
        return token

    async def _get_token_decimals(self, rpc_url: str, mint_address: str) -> Optional[int]:
        """Get token decimals from mint account."""
        try:
            from solana.rpc.async_api import AsyncClient
            from solders.pubkey import Pubkey

            if mint_address == NATIVE_SOL_ADDRESS:
                return 9

            async with AsyncClient(rpc_url) as client:
                mint_pubkey = Pubkey.from_string(mint_address)
                account_info = await client.get_account_info(mint_pubkey, encoding="jsonParsed")

                if account_info.value and account_info.value.data:
                    return account_info.value.data.parsed["info"]["decimals"]

        except Exception as e:
            logger.error(f"Error getting token decimals: {e}")

        return None

    async def _get_jupiter_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: Optional[int],
        user_public_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get quote from Jupiter API."""
        try:
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": str(amount),
                "dynamicSlippage": "true",
                "maxAccounts": "64"
            }

            if slippage_bps is not None:
                params["slippageBps"] = str(slippage_bps)
            if user_public_key:
                params["userPublicKey"] = user_public_key

            async with httpx.AsyncClient() as client:
                response = await client.get(JUPITER_QUOTE_ENDPOINT, params=params, timeout=30)
            quote_data = response.json()
            if "error" in quote_data:
                return {
                    "success": False,
                    "error": f"Jupiter quote error: {quote_data['error']}"
                }
            return {
                "success": True,
                "quote": quote_data
            }
        except Exception as e:
            logger.error(f"Error getting Jupiter quote: {e}")
            return {
                "success": False,
                "error": f"Failed to get quote: {str(e)}"
            }
    async def _get_jupiter_swap_transaction(
        self,
        quote: Dict[str, Any],
        user_public_key: str,
        priority_level: str
    ) -> Dict[str, Any]:
        """Get swap transaction from Jupiter API."""
        try:
            priority_fee = JUPITER_PRIORITY_LEVELS.get(priority_level, JUPITER_PRIORITY_LEVELS["veryHigh"])

            payload = {
                "quoteResponse": quote,
                "userPublicKey": user_public_key,
                "dynamicComputeUnitLimit": True,
                "dynamicSlippage": True,
                "priorityLevelWithMaxLamports": {
                    "maxLamports": priority_fee,
                    "priorityLevel": priority_level
                }
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    JUPITER_SWAP_ENDPOINT,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
            swap_data = response.json()
            return {
                "success": True,
                "swap_transaction": swap_data["swapTransaction"],
                "last_valid_block_height": swap_data.get("lastValidBlockHeight")
            }

        except Exception as e:
            logger.error(f"Error getting Jupiter swap transaction: {e}")
            return {
                "success": False,
                "error": f"Failed to get swap transaction: {str(e)}"
            }

    async def _execute_swap_transaction(
        self,
        rpc_url: str,
        wallet_keypair,
        swap_transaction_base64: str
    ) -> Dict[str, Any]:
        """Execute the swap transaction."""
        try:
            from solders.transaction import VersionedTransaction
            import base64

            transaction_bytes = base64.b64decode(swap_transaction_base64)
            transaction = VersionedTransaction.from_bytes(transaction_bytes)
            transaction.sign([wallet_keypair])

            return await self._submit_signed_transaction(rpc_url, transaction)

        except Exception as e:
            logger.error(f"Error executing swap transaction: {e}")
            error_msg = parse_transaction_error(str(e))
            return {
                "success": False,
                "error": error_msg
            }

    async def _submit_signed_transaction(self, rpc_url: str, transaction) -> Dict[str, Any]:
        """Send, confirm, and fetch fee information for a signed transaction."""

        async with AsyncClient(rpc_url) as client:
            # Send transaction
            response = await client.send_transaction(transaction)
            signature = str(response.value)

            # Wait for confirmation
            confirmation = await client.confirm_transaction(
                signature,
                commitment="confirmed"
            )
            fees = await self._extract_transaction_fees(client, signature)
            return {
                "success": True,
                "signature": signature,
                "fees": fees
            }

    async def _extract_transaction_fees(self, client, signature: str) -> Dict[str, Any]:
        try:
            tx_details = await client.get_transaction(
                signature,
                encoding="jsonParsed",
                commitment="confirmed",
                max_supported_transaction_version=0
            )

            if tx_details.value and tx_details.value.transaction.meta:
                fee_lamports = tx_details.value.transaction.meta.fee
                return {
                    "transaction_fee": fee_lamports,
                    "fee_sol": fee_lamports / 1_000_000_000
                }
        except Exception as e:
            logger.warning(f"Failed to get transaction fees: {e}")

        return {}

