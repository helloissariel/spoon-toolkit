# Spoon Toolkits - Comprehensive blockchain and cryptocurrency tools
__version__ = "0.1.0"

from .crypto.crypto_data_tools.predict_price import PredictPrice
from .crypto.crypto_data_tools.token_holders import TokenHolders
from .crypto.crypto_data_tools.trading_history import TradingHistory
from .crypto.crypto_data_tools.uniswap_liquidity import UniswapLiquidity
from .crypto.crypto_data_tools.wallet_analysis import WalletAnalysis
from .crypto.crypto_data_tools.price_data import GetTokenPriceTool, Get24hStatsTool, GetKlineDataTool
from .crypto.crypto_data_tools.price_alerts import PriceThresholdAlertTool, LpRangeCheckTool, SuddenPriceIncreaseTool
from .crypto.crypto_data_tools.lending_rates import LendingRateMonitorTool

from .crypto.crypto_powerdata import (
    CryptoPowerDataCEXTool,
    CryptoPowerDataDEXTool,
    CryptoPowerDataIndicatorsTool,
    CryptoPowerDataPriceTool,
    start_crypto_powerdata_mcp_stdio,
    start_crypto_powerdata_mcp_sse,
    start_crypto_powerdata_mcp_auto,
    CryptoPowerDataMCPServer,
    get_server_manager,
)

from .data_platforms.third_web.third_web_tools import (
    GetContractEventsFromThirdwebInsight,
    GetMultichainTransfersFromThirdwebInsight,
    GetTransactionsTool,
    GetContractTransactionsTool,
    GetContractTransactionsBySignatureTool,
    GetBlocksFromThirdwebInsight,
    GetWalletTransactionsFromThirdwebInsight
)

from .data_platforms.desearch.ai_search_official import search_ai_data, search_social_media, search_academic
from .data_platforms.desearch.builtin_tools import (
    DesearchAISearchTool,
    DesearchWebSearchTool,
    DesearchAcademicSearchTool,
    DesearchTwitterSearchTool
)

__all__ = [
    "PredictPrice",
    "TokenHolders",
    "TradingHistory",
    "UniswapLiquidity",
    "WalletAnalysis",
    "GetTokenPriceTool",
    "Get24hStatsTool",
    "GetKlineDataTool",
    "PriceThresholdAlertTool",
    "LpRangeCheckTool",
    "SuddenPriceIncreaseTool",
    "LendingRateMonitorTool",

    "GetContractEventsFromThirdwebInsight",
    "GetMultichainTransfersFromThirdwebInsight",
    "GetTransactionsTool",
    "GetContractTransactionsTool",
    "GetContractTransactionsBySignatureTool",
    "GetBlocksFromThirdwebInsight",
    "GetWalletTransactionsFromThirdwebInsight",

    # Crypto PowerData tools
    "CryptoPowerDataCEXTool",
    "CryptoPowerDataDEXTool",
    "CryptoPowerDataIndicatorsTool",
    "CryptoPowerDataPriceTool",
    "start_crypto_powerdata_mcp_stdio",
    "start_crypto_powerdata_mcp_sse",
    "start_crypto_powerdata_mcp_auto",
    "CryptoPowerDataMCPServer",
    "get_server_manager",

    # Desearch AI tools
    "search_ai_data",
    "search_social_media",
    "search_academic",

    # Desearch Builtin Tools
    "DesearchAISearchTool",
    "DesearchWebSearchTool",
    "DesearchAcademicSearchTool",
    "DesearchTwitterSearchTool",
]