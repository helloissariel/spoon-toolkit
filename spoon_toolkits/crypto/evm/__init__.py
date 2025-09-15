"""EVM toolkit tools for SpoonAI

This package provides EVM-related tools aligned with plugin-evm capabilities:
- Native token transfer
- Token swap (via aggregators)
- Cross-chain bridge (via LiFi)
- Governance actions (propose, vote, queue, execute)

All tools follow the BaseTool interface and are designed for readability and robustness.
"""

from .transfer import EvmTransferTool
from .swap import EvmSwapTool
from .bridge import EvmBridgeTool
from .erc20 import EvmErc20TransferTool
from .balance import EvmBalanceTool
from .quote import EvmSwapQuoteTool

__all__ = [
    "EvmTransferTool",
    "EvmSwapTool",
    "EvmBridgeTool",
    "EvmErc20TransferTool",
    "EvmBalanceTool",
    "EvmSwapQuoteTool",
]


