import httpx
import asyncio
import time
import logging
from typing import Dict, Any, Optional

try:
    from .env import DESEARCH_API_KEY, DESEARCH_BASE_URL, DESEARCH_TIMEOUT
except ImportError:
    from env import DESEARCH_API_KEY, DESEARCH_BASE_URL, DESEARCH_TIMEOUT

logger = logging.getLogger(__name__)

async def raise_on_4xx_5xx(response):
    await response.aread()
    response.raise_for_status()

desearch_client = httpx.AsyncClient(
    base_url=DESEARCH_BASE_URL.removesuffix('/'),
    headers={'Authorization': f"Bearer {DESEARCH_API_KEY}"},
    event_hooks={'response': [raise_on_4xx_5xx]},
    timeout=DESEARCH_TIMEOUT,
) 