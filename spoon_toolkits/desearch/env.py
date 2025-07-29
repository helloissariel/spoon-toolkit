import os
import dotenv
dotenv.load_dotenv()

DESEARCH_API_KEY = os.environ.get('DESEARCH_API_KEY', '')
DESEARCH_BASE_URL = os.environ.get('DESEARCH_BASE_URL', 'https://apis.desearch.ai')
DESEARCH_TIMEOUT = int(os.environ.get('DESEARCH_TIMEOUT', '30'))
DESEARCH_RETRY_COUNT = int(os.environ.get('DESEARCH_RETRY_COUNT', '3'))
DESEARCH_CACHE_TTL = int(os.environ.get('DESEARCH_CACHE_TTL', '300'))
DESEARCH_RATE_LIMIT = int(os.environ.get('DESEARCH_RATE_LIMIT', '100'))
DESEARCH_LOG_LEVEL = os.environ.get('DESEARCH_LOG_LEVEL', 'INFO') 