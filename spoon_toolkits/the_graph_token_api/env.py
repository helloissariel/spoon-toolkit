import os
import dotenv
dotenv.load_dotenv()

THE_GRAPH_TOKEN_API_JWT = os.environ.get('THE_GRAPH_TOKEN_API_JWT', "eyJh...")
HTTP_TIMEOUT_SECONDS = int(os.environ.get("HTTP_TIMEOUT_SECONDS", '30'))