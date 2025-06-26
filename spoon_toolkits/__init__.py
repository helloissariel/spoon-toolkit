# Spoon Toolkits - Comprehensive blockchain and cryptocurrency tools
__version__ = "0.1.0"

from .crypto.predict_price import PredictPrice
from .crypto.token_holders import TokenHolders
from .crypto.trading_history import TradingHistory
from .crypto.uniswap_liquidity import UniswapLiquidity
from .crypto.wallet_analysis import WalletAnalysis
from .crypto.price_data import GetTokenPriceTool, Get24hStatsTool, GetKlineDataTool
from .crypto.price_alerts import PriceThresholdAlertTool, LpRangeCheckTool, SuddenPriceIncreaseTool
from .crypto.lending_rates import LendingRateMonitorTool

from .fluence.fluence_tools import (
    FluenceListSSHKeysTool,
    FluenceCreateSSHKeyTool,
    FluenceDeleteSSHKeyTool,
    FluenceListVMsTool,
    FluenceCreateVMTool,
    FluenceDeleteVMTool,
    FluencePatchVMTool,
    FluenceListDefaultImagesTool,
    FluenceEstimateVMTool,
    FluenceListBasicConfigurationsTool,
    FluenceListCountriesTool,
    FluenceListHardwareTool,
    SearchFluenceMarketplaceOffers
)

from .third_web.third_web_tools import (
    GetContractEventsFromThirdwebInsight,
    GetMultichainTransfersFromThirdwebInsight,
    GetTransactionsTool,
    GetContractTransactionsTool,
    GetContractTransactionsBySignatureTool,
    GetBlocksFromThirdwebInsight,
    GetWalletTransactionsFromThirdwebInsight
)

__all__ = [
    "FluenceListSSHKeysTool",
    "FluenceCreateSSHKeyTool",
    "FluenceDeleteSSHKeyTool",
    "FluenceListVMsTool",
    "FluenceCreateVMTool",
    "FluenceDeleteVMTool",
    "FluencePatchVMTool",
    "FluenceListDefaultImagesTool",
    "FluenceEstimateVMTool",
    "FluenceListBasicConfigurationsTool",
    "FluenceListCountriesTool",
    "FluenceListHardwareTool",
    "SearchFluenceMarketplaceOffers",

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
    "GetWalletTransactionsFromThirdwebInsight"
]