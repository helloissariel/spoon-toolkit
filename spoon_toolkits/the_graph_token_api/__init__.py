# https://thegraph.com/docs/en/token-api/evm/get-balances-evm-by-address/
from fastmcp import FastMCP
from .balances_by_address import mcp as balances_by_address_server
from .historical_balances import mcp as historical_balances_server
from .nft import mcp as nft_server
from .ohlcv import mcp as ohlcv_server
from .swap_events import mcp as swap_events_server
from .token_holders import mcp as token_holders_server
from .token_metadata import mcp as token_metadata_server
from .transfer_events import mcp as transfer_events_server

mcp_server = FastMCP("TheGraphTokenApiServer")
mcp_server.mount(balances_by_address_server, "BalancesByAddress")
mcp_server.mount(historical_balances_server, "HistoricalBalances")
mcp_server.mount(nft_server, "Nft")
mcp_server.mount(ohlcv_server, "Ohlcv")
mcp_server.mount(swap_events_server, "SwapEvents")
mcp_server.mount(token_holders_server, "TokenHolders")
mcp_server.mount(token_metadata_server, "TokenMetadata")
mcp_server.mount(transfer_events_server, "TransferEvents")

if __name__ == "__main__":
    # mcp_server.run(host='0.0.0.0', port=8000)
    mcp_server.run()