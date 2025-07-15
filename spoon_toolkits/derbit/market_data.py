from fastmcp import FastMCP
from .http_client import derbit_client

mcp = FastMCP("MarketData")

@mcp.tool()
async def get_apr_history(currency: str, limit: int = 5) -> dict:
    """
    Retrieves historical APR data for specified currency. Only applicable to yield-generating tokens (USDE, STETH).
    {
      "jsonrpc": "2.0",
      "id": 1,
      "result": {
        "data": [
          {
            "day": 20200,
            "apr": 2.814
          },
          {
            "day": 20199,
            "apr": 2.749
          },
          {
            "day": 20198,
            "apr": 2.684
          },
          {
            "day": 20197,
            "apr": 2.667
          },
          {
            "day": 20196,
            "apr": 2.722
          }
        ],
        "continuation": 20196
      }
    }
    """
    r = await derbit_client.get(f'/public/get_apr_history?currency={currency}&limit={limit}')
    r = r.json()
    r = r["result"]
    return r

@mcp.tool()
async def get_book_summary_by_currency(currency: str, kind: str) -> dict:
    """
    Retrieves the summary information such as open interest, 24h volume, etc. for all instruments for the currency (optionally filtered by kind).
    currency: BTC,ETH,USDC,USDT,EURR
    kind: future,option,spot,future_combo,option_combo
    {
      "jsonrpc": "2.0",
      "id": 9344,
      "result": [
        {
          "volume_usd": 0,
          "volume": 0,
          "quote_currency": "USD",
          "price_change": -11.1896349,
          "open_interest": 0,
          "mid_price": null,
          "mark_price": 3579.73,
          "mark_iv": 80,
          "low": null,
          "last": null,
          "instrument_name": "BTC-22FEB19",
          "high": null,
          "estimated_delivery_price": 3579.73,
          "creation_timestamp": 1550230036440,
          "bid_price": null,
          "base_currency": "BTC",
          "ask_price": null
        },
        {
          "volume_usd": 22440,
          "volume": 6.24,
          "quote_currency": "USD",
          "price_change": -60.8183509,
          "open_interest": 183180,
          "mid_price": null,
          "mark_price": 3579.73,
          "mark_iv": 80,
          "low": 3591,
          "last": 3595,
          "instrument_name": "BTC-PERPETUAL",
          "high": 3595,
          "funding_8h": 0.0002574,
          "estimated_delivery_price": 3579.73,
          "current_funding": 0,
          "creation_timestamp": 1550230036440,
          "bid_price": null,
          "base_currency": "BTC",
          "ask_price": null
        }
      ]
    }
    """
    r = await derbit_client.get(f'/public/get_book_summary_by_currency?currency={currency}&kind={kind}')
    r = r.json()
    r = r["result"]
    return r

@mcp.tool()
async def get_book_summary_by_instrument(instrument_name: str) -> dict:
    """
    Retrieves the summary information such as open interest, 24h volume, etc. for a specific instrument.
    instrument_name example: ETH-22FEB19-140-P
    {
      "jsonrpc": "2.0",
      "id": 3659,
      "result": [
        {
          "volume": 0.55,
          "underlying_price": 121.38,
          "underlying_index": "index_price",
          "quote_currency": "USD",
          "price_change": -26.7793594,
          "open_interest": 0.55,
          "mid_price": 0.2444,
          "mark_price": 0.179112,
          "mark_price": 80,
          "low": 0.34,
          "last": 0.34,
          "interest_rate": 0.207,
          "instrument_name": "ETH-22FEB19-140-P",
          "high": 0.34,
          "creation_timestamp": 1550227952163,
          "bid_price": 0.1488,
          "base_currency": "ETH",
          "ask_price": 0.34
        }
      ]
    }
    """
    r = await derbit_client.get(f'/public/get_book_summary_by_instrument?instrument_name={instrument_name}')
    r = r.json()
    r = r["result"]
    return r

async def get_contract_size(instrument_name: str):
    """
    Retrieves the contract size of provided instrument.
    instrument_name example: ETH-22FEB19-140-P
    {
        "jsonrpc": "2.0",
        "result": {
            "contract_size": 10
        }
    }
    """
    r = await derbit_client.get(f'/public/get_contract_size?instrument_name={instrument_name}')
    r = r.json()
    r = r["result"]
    return r

async def get_currencies():
    """
    Retrieves all cryptocurrencies supported by the API.
    {
      "jsonrpc": "2.0",
      "id": 7538,
      "result": [
          {
              "coin_type": "ETHER",
              "currency": "ETH",
              "currency_long": "Ethereum",
              "fee_precision": 4,
              "min_confirmations": 1,
              "min_withdrawal_fee": 0.0001,
              "withdrawal_fee": 0.0006,
              "withdrawal_priorities": []
          },
          {
              "coin_type": "BITCOIN",
              "currency": "BTC",
              "currency_long": "Bitcoin",
              "fee_precision": 4,
              "min_confirmations": 1,
              "min_withdrawal_fee": 0.0001,
              "withdrawal_fee": 0.0001,
              "withdrawal_priorities": [
                  {
                      "value": 0.15,
                      "name": "very_low"
                  },
                  {
                      "value": 1.5,
                      "name": "very_high"
                  }
              ]
          }
      ]
    }
    """
    r = await derbit_client.get(f'/public/get_currencies')
    r = r.json()
    r = r["result"]
    return r

async def get_delivery_prices(index_name: str, offset: int = 0, count: int = 10):
    """
    Retrieves delivery prices for then given index
    index_name: btc_usd,eth_usd,ada_usdc,algo_usdc,avax_usdc,bch_usdc,bnb_usdc,btc_usdc,btcdvol_usdc,buidl_usdc,doge_usdc,dot_usdc,eurr_usdc,eth_usdc,ethdvol_usdc,link_usdc,ltc_usdc,near_usdc,paxg_usdc,shib_usdc,sol_usdc,steth_usdc,trump_usdc,trx_usdc,uni_usdc,usde_usdc,usyc_usdc,xrp_usdc,btc_usdt,eth_usdt,eurr_usdt,sol_usdt,steth_usdt,usdc_usdt,usde_usdt,btc_eurr,btc_usde,btc_usyc,eth_btc,eth_eurr,eth_usde,eth_usyc,steth_eth,paxg_btc
    {
      "jsonrpc": "2.0",
      "id": 3601,
      "result": {
        "data": [
          {
            "date": "2020-01-02",
            "delivery_price": 7131.214606410254
          },
          {
            "date": "2019-12-21",
            "delivery_price": 7150.943217777777
          },
          {
            "date": "2019-12-20",
            "delivery_price": 7175.988445532345
          },
          {
            "date": "2019-12-19",
            "delivery_price": 7189.540776143791
          },
          {
            "date": "2019-12-18",
            "delivery_price": 6698.353743857118
          }
        ],
        "records_total": 58
      }
    }
    """
    r = await derbit_client.get(f"/public/get_delivery_prices?count={count}&index_name={index_name}&offset={offset}")
    r = r.json()
    r = r["result"]
    return r
