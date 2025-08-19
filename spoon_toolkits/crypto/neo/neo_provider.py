"""Neo blockchain data provider

This module provides a comprehensive interface for interacting with the Neo blockchain
through the OneGate API. It supports both mainnet and testnet networks and includes
various utility methods for data processing and validation.

The provider handles:
- Address validation and conversion
- Asset amount formatting
- JSON serialization
- Safe dictionary access
- Network-specific API endpoints
"""

import json
import requests
from typing import Dict, Any, List
from decimal import Decimal
import neo3.wallet.utils

# API URLs for different networks
MAINNET_URL = "https://explorer.onegate.space/api"
TESTNET_URL = "https://testmagnet.explorer.onegate.space/api"

class NeoProvider:
    """Neo blockchain data provider for interacting with OneGate API
    
    This class provides a unified interface for querying Neo blockchain data
    including addresses, assets, blocks, transactions, and smart contracts.
    
    Attributes:
        network (str): The Neo network to connect to ('mainnet' or 'testnet')
        url (str): The API endpoint URL for the selected network
        _session (requests.Session): HTTP session for API requests
    """
    
    def __init__(self, network: str = "testnet"):
        """Initialize the Neo provider
        
        Args:
            network (str): The Neo network to connect to. Must be 'mainnet' or 'testnet'
        
        Raises:
            ValueError: If network is not 'mainnet' or 'testnet'
        """
        if network not in ["mainnet", "testnet"]:
            raise ValueError("Network must be 'mainnet' or 'testnet'")
        
        self.network = network
        self.url = MAINNET_URL if network == "mainnet" else TESTNET_URL
        self._session = requests.Session()
    
    def _make_request(self, method: str, params: dict) -> dict:
        """Send RPC request to Neo API
        
        Args:
            method (str): The RPC method name to call
            params (dict): Parameters for the RPC method
            
        Returns:
            dict: The JSON response from the API
            
        Raises:
            Exception: If the API request fails or returns an error
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        
        try:
            response = self._session.post(self.url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _validate_address(self, address: str) -> str:
        """Validate and convert address format
        
        Converts Neo addresses to script hash format if they are in standard format.
        If the address is already in script hash format, it returns as is.
        
        Args:
            address (str): The address to validate and convert
            
        Returns:
            str: The address in script hash format (0x...)
            
        Raises:
            ValueError: If the address is not a valid Neo address
        """
        if neo3.wallet.utils.is_valid_address(address):
            return "0x" + neo3.wallet.utils.address_to_script_hash(address=address).__str__()
        return address
    
    def _handle_response(self, response: dict) -> dict:
        """Handle API response and extract result
        
        Args:
            response (dict): The JSON response from the API
            
        Returns:
            dict: The result data from the response
            
        Raises:
            Exception: If the response contains an error or invalid format
        """
        if "error" in response:
            raise Exception(f"API error: {response['error']}")
        
        if "result" not in response:
            raise Exception("Invalid API response format")
        
        return response["result"]
    
    def _convert_asset_amount(self, amount_string: str, decimals: int) -> Decimal:
        """Convert asset amount string to decimal with proper decimal places
        
        Args:
            amount_string (str): The amount as a string
            decimals (int): The number of decimal places for the asset
            
        Returns:
            Decimal: The converted amount with proper decimal places
            
        Raises:
            ValueError: If the amount string is invalid
        """
        try:
            amount = Decimal(amount_string)
            return amount / (10 ** decimals)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid amount string: {amount_string}")
    
    def _format_amount(self, amount: Decimal, decimals: int = 8) -> str:
        """Format amount with specified decimal places
        
        Args:
            amount (Decimal): The amount to format
            decimals (int): The number of decimal places to use
            
        Returns:
            str: The formatted amount string
        """
        return f"{amount:.{decimals}f}"
    
    def _to_json(self, obj: Any) -> str:
        """Convert object to JSON string
        
        Args:
            obj: The object to serialize
            
        Returns:
            str: The JSON string representation
        """
        return json.dumps(obj, default=lambda obj: obj.__dict__)
    
    # Address-related methods
    async def get_active_addresses(self, days: int) -> List[int]:
        """Get active addresses count for specified days
        
        Args:
            days (int): Number of days to get active address counts for
            
        Returns:
            List[int]: List of daily active address counts
        """
        response = self._make_request("GetActiveAddresses", {"Days": days})
        result = self._handle_response(response)
        
        if isinstance(result, list):
            return [item["ActiveAddresses"] for item in result if "ActiveAddresses" in item]
        return []
    
    async def get_address_info(self, address: str) -> Dict[str, Any]:
        """Get address information
        
        Args:
            address (str): The Neo address to get information for
            
        Returns:
            Dict[str, Any]: Address information including first use time, last use time, etc.
        """
        validated_address = self._validate_address(address)
        response = self._make_request("GetAddressInfoByAddress", {"Address": validated_address})
        return self._handle_response(response)
    
    async def get_address_count(self) -> int:
        """Get total address count
        
        Returns:
            int: Total number of addresses on the network
        """
        response = self._make_request("GetAddressCount", {})
        return self._handle_response(response)
    
    # Block-related methods
    async def get_block_info(self, block_hash: str) -> Dict[str, Any]:
        """Get block information by hash
        
        Args:
            block_hash (str): The block hash to get information for
            
        Returns:
            Dict[str, Any]: Block information including transactions, timestamp, etc.
        """
        response = self._make_request("GetBlockByHash", {"BlockHash": block_hash})
        return self._handle_response(response)
    
    async def get_block_by_height(self, block_height: int) -> Dict[str, Any]:
        """Get block information by height
        
        Args:
            block_height (int): The block height to get information for
            
        Returns:
            Dict[str, Any]: Block information including transactions, timestamp, etc.
        """
        response = self._make_request("GetBlockByHeight", {"BlockHeight": block_height})
        return self._handle_response(response)
    
    async def get_block_count(self) -> int:
        """Get total block count
        
        Returns:
            int: Total number of blocks on the network
        """
        response = self._make_request("GetBlockCount", {})
        return self._handle_response(response)
    
    # Transaction-related methods
    async def get_transaction_info(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction information
        
        Args:
            tx_hash (str): The transaction hash to get information for
            
        Returns:
            Dict[str, Any]: Transaction information including inputs, outputs, etc.
        """
        response = self._make_request("GetRawTransactionByTransactionHash", {"TransactionHash": tx_hash})
        return self._handle_response(response)
    
    async def get_transaction_count(self) -> int:
        """Get total transaction count
        
        Returns:
            int: Total number of transactions on the network
        """
        response = self._make_request("GetTransactionCount", {})
        return self._handle_response(response)
    
    # Asset-related methods
    async def get_asset_info(self, asset_hash: str) -> Dict[str, Any]:
        """Get asset information by hash
        
        Args:
            asset_hash (str): The asset hash to get information for
            
        Returns:
            Dict[str, Any]: Asset information including name, symbol, decimals, etc.
        """
        response = self._make_request("GetAssetInfoByHash", {"AssetHash": asset_hash})
        return self._handle_response(response)
    
    async def get_asset_count(self) -> int:
        """Get total asset count
        
        Returns:
            int: Total number of assets on the network
        """
        response = self._make_request("GetAssetCount", {})
        return self._handle_response(response)
    
    # Contract-related methods
    async def get_contract_info(self, contract_hash: str) -> Dict[str, Any]:
        """Get contract information by hash
        
        Args:
            contract_hash (str): The contract hash to get information for
            
        Returns:
            Dict[str, Any]: Contract information including name, hash, etc.
        """
        response = self._make_request("GetContractByHash", {"ContractHash": contract_hash})
        return self._handle_response(response)
    
    async def get_contract_count(self) -> int:
        """Get total contract count
        
        Returns:
            int: Total number of contracts on the network
        """
        response = self._make_request("GetContractCount", {})
        return self._handle_response(response)
    
    def __enter__(self):
        """Context manager entry point"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - closes the HTTP session"""
        self._session.close() 