from fastmcp import FastMCP
from .http_client import the_graph_token_api_client
from .utils import normalize_ethereum_contract_address

mcp = FastMCP("TheGraphTokenApiTokenMetadata")

@mcp.tool()
async def token_metadata(contract: str, network_id: str = "mainnet"):
    """
    Get the metadata of an ERC-20 token contract address.
    network_id: arbitrum-one, avalanche, base, bsc, mainnet, matic, optimism, unichain
    {
      "data": [
        {
          "block_num": 22589353,
          "datetime": "2025-05-29 15:40:11",
          "address": "0xc944e90c64b2c07662a292be6244bdf05cda44a7",
          "decimals": 18,
          "symbol": "GRT",
          "name": "Graph Token",
          "circulating_supply": "16667753581.233711",
          "holders": 139562,
          "network_id": "mainnet",
          "icon": {
            "web3icon": "GRT"
          }
        }
      ]
    }
    """
    contract = normalize_ethereum_contract_address(contract)
    resp = await the_graph_token_api_client.get(f"/tokens/evm/{contract}?network_id={network_id}")
    resp = resp.json()
    return resp