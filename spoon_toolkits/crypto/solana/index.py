from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional, Sequence

from .constants import SOLANA_SERVICE_NAME
from .integration import RuntimeServiceDiscovery
from .service import SolanaService
from .swap import SolanaSwapTool
from .transfer import SolanaTransferTool
from .wallet import SolanaWalletInfoTool

logger = logging.getLogger(__name__)

async def _noop_init(*_args: Any, **_kwargs: Any) -> None:
    """Default no-op init used when callers do not supply an init hook."""

@dataclass(frozen=True)
class ProviderDefinition:
    """Define a provider entry compatible with the TypeScript plugin schema."""

    name: str
    description: str
    getter: Callable[..., Awaitable[Dict[str, Any]]]
    dynamic: bool = True

    async def get(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return await self.getter(*args, **kwargs)


@dataclass(frozen=True)
class PluginManifest:

    name: str
    description: str
    actions: Sequence[Any] = field(default_factory=list)
    evaluators: Sequence[Any] = field(default_factory=list)
    providers: Sequence[ProviderDefinition] = field(default_factory=list)
    services: Sequence[Any] = field(default_factory=list)
    init: Callable[..., Awaitable[None]] = field(default=_noop_init)

    async def initialize(self, context: Any = None, runtime: Any = None) -> None:
        await self.init(context, runtime)

    def to_dict(self) -> Dict[str, Any]:
        """Return the manifest as a plain dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "actions": list(self.actions),
            "evaluators": list(self.evaluators),
            "providers": list(self.providers),
            "services": list(self.services),
            "init": self.init,
        }

def _get_agent_name(runtime: Any, state: Any) -> str:
    """Extract a human-readable agent name from runtime or state."""
    if state is not None:
        for key in ("agent_name", "agentName"):
            if isinstance(state, dict) and key in state:
                return str(state[key])
            value = getattr(state, key, None)
            if value:
                return str(value)
    if runtime is not None:
        for attr in ("character", "agent"):
            candidate = getattr(runtime, attr, None)
            if candidate:
                name = getattr(candidate, "name", None)
                if name:
                    return str(name)
        name = getattr(runtime, "name", None)
        if name:
            return str(name)
    return "Agent"


async def wallet_provider(
    runtime: Any,
    _message: Any = None,
    state: Any = None,
) -> Dict[str, Any]:
    """Return structured wallet information for context injection."""
    tool = SolanaWalletInfoTool()
    result = await tool.execute()

    if result.error:
        logger.info("solana-wallet provider unavailable: %s", result.error)
        return {
            "data": None,
            "values": {},
            "text": "",
            "error": result.error,
        }

    wallet = result.output or {}
    address = wallet.get("address") or ""
    truncated = wallet.get("truncated_address") or address[-8:] if address else ""
    sol_balance = wallet.get("sol_balance", 0)
    token_count = int(wallet.get("token_count", 0) or 0)
    tokens = wallet.get("tokens") or []

    values: Dict[str, str] = {
        "address": address,
        "truncated_address": truncated,
        "sol_balance": f"{sol_balance}",
        "token_count": str(token_count),
    }

    lines = [
        "",
        "",
        f"{_get_agent_name(runtime, state)}'s Solana Wallet {f'({truncated})' if truncated else ''}".strip(),
        f"SOL Balance: {sol_balance}",
    ]

    if tokens:
        lines.append("")
        lines.append("Token Balances:")
        for index, token in enumerate(tokens):
            mint = token.get("mint", "")
            balance = token.get("balance", token.get("ui_amount", 0))
            decimals = token.get("decimals", "")
            values[f"token_{index}_mint"] = mint
            values[f"token_{index}_balance"] = f"{balance}"
            if decimals != "":
                values[f"token_{index}_decimals"] = str(decimals)
            lines.append(f"- {mint}: {balance}")
    else:
        lines.append("No SPL token balances available.")

    text = "\n".join(lines)

    return {
        "data": wallet,
        "values": values,
        "text": text,
    }

async def init_plugin(_context: Any = None, runtime: Any = None) -> None:
    """Initialise Solana plugin behaviour with the provided runtime."""
    if runtime is None:
        logger.warning("Solana plugin init called without runtime; skipping registration")
        return

    logger.info("Solana plugin initialising")
    discovery = RuntimeServiceDiscovery(
        runtime,
        service_type="TRADER_CHAIN",
        poll_interval=1.0,
        timeout=None,
        log_prefix="solana",
    )

    try:
        trader_chain_service = await discovery.wait_for_service()
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Failed to acquire TRADER_CHAIN service: %s", exc)
        return

    register_fn: Optional[Callable[[Dict[str, Any]], Any]] = None
    for attr in ("register_chain", "registerChain"):
        candidate = getattr(trader_chain_service, attr, None)
        if callable(candidate):
            register_fn = candidate
            break

    if register_fn is None:
        logger.warning("TRADER_CHAIN service does not expose a register_chain method")
        return

    details = {
        "name": "Solana services",
        "chain": "solana",
        "service": SOLANA_SERVICE_NAME,
    }

    try:
        maybe_coro = register_fn(details)
        if hasattr(maybe_coro, "__await__"):
            await maybe_coro  # type: ignore[func-returns-value]
        logger.info("Solana plugin registered with TRADER_CHAIN service")
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Failed to register Solana chain with trader service: %s", exc)

solana_plugin = PluginManifest(
    name=SOLANA_SERVICE_NAME,
    description="Solana Plugin for SpoonAI (Python port)",
    actions=[
        SolanaTransferTool(),
        SolanaSwapTool(),
    ],
    evaluators=[],
    providers=[
        ProviderDefinition(
            name="solana-wallet",
            description="Access Solana wallet information and balances.",
            getter=wallet_provider,
            dynamic=True,
        )
    ],
    services=[SolanaService],
    init=init_plugin,
)


__all__ = [
    "PluginManifest",
    "ProviderDefinition",
    "solana_plugin",
    "wallet_provider",
    "init_plugin",
]
