"""Solana toolkit for SpoonAI"""

# Transfer Tools
from .transfer import SolanaTransferTool, SolanaBatchTransferTool

# Swap Tools
from .swap import (
    SolanaSwapTool,
    SolanaSwapQuoteTool,
    SolanaOptimalTradeCalculatorTool
)


# Wallet Management Tools
from .wallet import (
    SolanaCreateWalletTool,
    SolanaImportWalletTool,
    SolanaWalletInfoTool,
    SolanaValidateAddressTool,
    SolanaMultiWalletTool,
    SolanaWalletHistoryTool,
    SolanaBatchWalletTool,
    SolanaWalletFormatterTool
)

# Blockchain Service Tools
from .service import (
    SolanaNetworkInfoTool,
    SolanaBlockTool,
    SolanaTransactionTool,
    SolanaProgramTool,
    SolanaMarketDataTool,
    SolanaAddressTypeTool,
    SolanaAccountMonitorTool,
    get_wallet_cache_scheduler,
    get_rpc_url,
    validate_solana_address,
    validate_private_key,
    get_api_key,
    lamports_to_sol,
    sol_to_lamports,
    format_token_amount,
    parse_token_amount,
    is_native_sol,
    verify_solana_signature,
    detect_pubkeys_from_string,
    detect_private_keys_from_string,
    create_request_headers,
    parse_transaction_error,
    truncate_address,
    SolanaSignatureVerifyTool,
    SolanaKeysDetectionTool,
)
from .keypairUtils import (
    get_wallet_keypair,
    get_wallet_key,
    get_private_key,
    get_public_key,
)
from .index import (
    solana_plugin,
    PluginManifest,
    ProviderDefinition,
    wallet_provider,
    init_plugin,
)
from .plugin_service import SolanaPluginService
from .environment import (
    load_solana_config,
    SolanaConfig,
)
from .constants import (
    NATIVE_SOL_ADDRESS,
    TOKEN_ADDRESSES,
    DEFAULT_SLIPPAGE_BPS,
    JUPITER_PRIORITY_LEVELS
)

from .types import (
    WalletPortfolio,
    Item,
    Prices,
    TransferContent,
    SwapContent,
    KeypairResult,
    TokenMetadata
)

# Export all tools for easy access
__all__ = [

    # Transfer Tools
    "SolanaTransferTool",
    "SolanaBatchTransferTool",

    # Swap Tools
    "SolanaSwapTool",
    "SolanaSwapQuoteTool",
    "SolanaOptimalTradeCalculatorTool",


   

    # Wallet Tools
    "SolanaCreateWalletTool",
    "SolanaImportWalletTool",
    "SolanaWalletInfoTool",
    "SolanaValidateAddressTool",
    "SolanaMultiWalletTool",
    "SolanaWalletHistoryTool",
    "SolanaBatchWalletTool",
    "SolanaWalletFormatterTool",

    # Service Tools
    "SolanaNetworkInfoTool",
    "SolanaBlockTool",
    "SolanaTransactionTool",
    "SolanaProgramTool",
    "SolanaMarketDataTool",
    "SolanaAddressTypeTool",
    "SolanaAccountMonitorTool",
    "get_wallet_cache_scheduler",


    
    # Constants
    "NATIVE_SOL_ADDRESS",
    "TOKEN_ADDRESSES",
    "DEFAULT_SLIPPAGE_BPS",
    "JUPITER_PRIORITY_LEVELS",

    # Types
    "WalletPortfolio",
    "Item",
    "Prices",
    "TransferContent",
    "SwapContent",
    "KeypairResult",
    "TokenMetadata"
]
