"""Solana toolkit constants，This module defines constants used throughout the Solana toolkit"""

# Service and Cache Configuration
SOLANA_SERVICE_NAME = "chain_solana"
SOLANA_WALLET_DATA_CACHE_KEY = "solana/walletData"

# Default RPC Endpoints
DEFAULT_SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
HELIUS_RPC_URL = "https://rpc.helius.xyz"

# Network Configuration
LAMPORTS_PER_SOL = 1_000_000_000
SOLANA_DEVNET_RPC = "https://api.devnet.solana.com"
SOLANA_TESTNET_RPC = "https://api.testnet.solana.com"

# Token Program IDs
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022_PROGRAM_ID = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
ASSOCIATED_TOKEN_PROGRAM_ID = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"

# System Program ID
SYSTEM_PROGRAM_ID = "11111111111111111111111111111111"

# Metadata Program ID (Metaplex)
METADATA_PROGRAM_ID = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"

# Well-known Token Addresses
TOKEN_ADDRESSES = {
    "SOL": "So11111111111111111111111111111111111111112",  # Wrapped SOL
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT
    "BTC": "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E",   # Wormhole Wrapped BTC
    "ETH": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",   # Wrapped ETH
}

# Native SOL placeholder address (used for swaps)
NATIVE_SOL_ADDRESS = "So11111111111111111111111111111111111111112"

# Jupiter API Configuration
JUPITER_API_BASE_URL = "https://quote-api.jup.ag/v6"
JUPITER_QUOTE_ENDPOINT = f"{JUPITER_API_BASE_URL}/quote"
JUPITER_SWAP_ENDPOINT = f"{JUPITER_API_BASE_URL}/swap"

# Birdeye API Configuration
BIRDEYE_API_BASE_URL = "https://public-api.birdeye.so"
BIRDEYE_PRICE_ENDPOINT = f"{BIRDEYE_API_BASE_URL}/defi/price"
BIRDEYE_WALLET_ENDPOINT = f"{BIRDEYE_API_BASE_URL}/v1/wallet/token_list"

# Transaction Configuration
DEFAULT_PRIORITY_FEE = 5  # micro-lamports per compute unit
MAX_RETRIES = 3
RETRY_DELAY = 2.0  # seconds

# Slippage Configuration
DEFAULT_SLIPPAGE_BPS = 100  # 1%
MAX_SLIPPAGE_BPS = 3000     # 30%

# Cache Configuration
UPDATE_INTERVAL = 120  # seconds
CACHE_TTL = 300       # seconds

# Account Data Lengths
TOKEN_ACCOUNT_DATA_LENGTH = 165
TOKEN_MINT_DATA_LENGTH = 82

# Error Messages
ERROR_MESSAGES = {
    "INVALID_ADDRESS": "Invalid Solana address format",
    "INVALID_PRIVATE_KEY": "Invalid private key format",
    "INSUFFICIENT_BALANCE": "Insufficient balance for transaction",
    "NETWORK_ERROR": "Failed to connect to Solana network",
    "TRANSACTION_FAILED": "Transaction failed to execute",
    "SLIPPAGE_EXCEEDED": "Transaction failed due to slippage tolerance exceeded",
    "TOKEN_NOT_FOUND": "Token not found",
    "INVALID_AMOUNT": "Invalid amount specified",
}

# Environment Variable Keys
ENV_KEYS = {
    "RPC_URL": ["SOLANA_RPC_URL", "RPC_URL"],
    "PRIVATE_KEY": ["SOLANA_PRIVATE_KEY", "WALLET_PRIVATE_KEY"],
    "PUBLIC_KEY": ["SOLANA_PUBLIC_KEY", "WALLET_PUBLIC_KEY"],
    "HELIUS_API_KEY": ["HELIUS_API_KEY"],
    "BIRDEYE_API_KEY": ["BIRDEYE_API_KEY"],
}

# Priority Levels for Jupiter
JUPITER_PRIORITY_LEVELS = {
    "low": 50,
    "medium": 200,
    "high": 1000,
    "veryHigh": 4_000_000,
}
