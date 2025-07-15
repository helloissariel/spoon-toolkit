import httpx
import asyncio
from .env import DERBIT_CLIENT_ID, DERBIT_CLIENT_SECRET
import time

_derbit_init_time: float = time.time()  # timestamp in seconds
_derbit_token_expire_time: int = 0

async def raise_on_4xx_5xx(response: httpx.Response):
    if response.status_code == 401 or (time.time() - _derbit_init_time) * 2 > _derbit_token_expire_time:
        await get_auth_token()
    await response.aread()
    response.raise_for_status()

derbit_client = httpx.AsyncClient(
    base_url='https://test.deribit.com/api/v2'.removesuffix('/'),
    event_hooks={'response': [raise_on_4xx_5xx]},
)

async def get_auth_token():
    resp = await derbit_client.get(f"/public/auth?client_id={DERBIT_CLIENT_ID}&client_secret={DERBIT_CLIENT_SECRET}&grant_type=client_credentials")
    resp = resp.json()
    """
    {
      "jsonrpc": "2.0",
      "id": 9929,
      "result": {
          "access_token": "1582628593469.1MbQ-J_4.CBP-OqOwm_FBdMYj4cRK2dMXyHPfBtXGpzLxhWg31nHu3H_Q60FpE5_vqUBEQGSiMrIGzw3nC37NMb9d1tpBNqBOM_Ql9pXOmgtV9Yj3Pq1c6BqC6dU6eTxHMFO67x8GpJxqw_QcKP5IepwGBD-gfKSHfAv9AEnLJkNu3JkMJBdLToY1lrBnuedF3dU_uARm",
          "expires_in": 31536000,
          "refresh_token": "1582628593469.1GP4rQd0.A9Wa78o5kFRIUP49mScaD1CqHgiK50HOl2VA6kCtWa8BQZU5Dr03BhcbXPNvEh3I_MVixKZXnyoBeKJwLl8LXnfo180ckAiPj3zOclcUu4zkXuF3NNP3sTPcDf1B3C1CwMKkJ1NOcf1yPmRbsrd7hbgQ-hLa40tfx6Oa-85ymm_3Z65LZcnCeLrqlj_A9jM",
          "scope": "connection mainaccount",
          "enabled_features": [],
          "token_type": "bearer"
      }
    }
    """
    access_token = resp["result"]["access_token"]
    derbit_client.headers.update({"Authorization": f"Bearer {access_token}"})
    global _derbit_token_expire_time
    _derbit_token_expire_time = resp["result"]["expires_in"]

loop = asyncio.get_running_loop()
loop.run_until_complete(get_auth_token())
