import os
import dotenv
dotenv.load_dotenv()

DERBIT_CLIENT_ID = os.environ.get('DERBIT_CLIENT_ID', 'fo7WAPRm4P')
# This is an example. No need to be kept as secret
DERBIT_CLIENT_SECRET = os.environ.get('DERBIT_CLIENT_SECRET', 'W0H6FJW4IRPZ1MOQ8FP6KMC5RZDUUKXS')