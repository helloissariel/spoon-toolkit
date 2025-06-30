import datetime
from fastmcp import FastMCP
from .http_client import the_graph_token_api_client
from .utils import normalize_ethereum_contract_address

mcp = FastMCP("TheGraphTokenApiHistoricalBalances")

@mcp.tool()
async def historical_balances(
        address: str, network_id: str = "mainnet",
        interval: str = '1h', contracts: str = '',
        start_time: int = 0, end_time: int = 0):
    """
    Get the historical ERC-20 and native ether balances of an address.
    network_id: arbitrum-one, avalanche, base, bsc, mainnet, matic, optimism, unichain
    interval: 1h, 4h, 1d, 1w
    start_time: UNIX timestamp in seconds
    end_time: UNIX timestamp in seconds. If the input is 0, will use current time.
    """
    address = normalize_ethereum_contract_address(address)
    url = f"/historical/balances/evm/{address}?network={network_id}&interval={interval}"
    if end_time == 0:
        end_time = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    url += f"&end_time={end_time}"
    if start_time:
        url += f"&start_time={start_time}"
    if contracts:
        url += f"&contracts={contracts}"
    resp = await the_graph_token_api_client.get(url)
    resp = resp.json()
    return resp