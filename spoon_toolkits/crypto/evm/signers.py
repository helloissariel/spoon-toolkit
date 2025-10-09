"""
Unified signer interface for EVM tools supporting both local private key and Turnkey signing.

This module provides a clean abstraction for transaction signing, allowing EVM tools
to work with either local private keys (via web3.py) or Turnkey's secure API.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Union

from web3 import Web3
from eth_account import Account as EthAccount

from spoon_ai.tools.base import ToolResult

logger = logging.getLogger(__name__)


class SignerError(Exception):
    """Exception raised for signing-related errors."""
    pass


class EvmSigner(ABC):
    """Abstract base class for EVM transaction signers."""

    @abstractmethod
    async def sign_transaction(self, tx_dict: Dict[str, Any], rpc_url: str) -> str:
        """
        Sign an EVM transaction.

        Args:
            tx_dict: Transaction dictionary ready for signing
            rpc_url: RPC URL for chain connection (may be used for chain_id resolution)

        Returns:
            Hex string of the signed transaction
        """
        pass

    @abstractmethod
    async def get_address(self) -> str:
        """
        Get the signer's address.

        Returns:
            Hex address string
        """
        pass

    @property
    @abstractmethod
    def signer_type(self) -> str:
        """Return the type of signer ('local' or 'turnkey')."""
        pass


class LocalSigner(EvmSigner):
    """Signer using local private key via web3.py."""

    def __init__(self, private_key: str):
        """
        Initialize with private key.

        Args:
            private_key: Private key as hex string (0x-prefixed)
        """
        if not private_key or not private_key.startswith("0x"):
            raise ValueError("Invalid private key format")
        self.private_key = private_key
        self._account = EthAccount.from_key(private_key)

    async def sign_transaction(self, tx_dict: Dict[str, Any], rpc_url: str) -> str:
        """Sign transaction using local private key."""
        try:
            signed = self._account.sign_transaction(tx_dict)
            return signed.raw_transaction.hex()
        except Exception as e:
            raise SignerError(f"Local signing failed: {str(e)}")

    async def get_address(self) -> str:
        """Get the account address."""
        return self._account.address

    @property
    def signer_type(self) -> str:
        return "local"


class TurnkeySigner(EvmSigner):
    """Signer using Turnkey API for secure key management."""

    def __init__(self, sign_with: str, turnkey_client=None):
        """
        Initialize with Turnkey signing identity.

        Args:
            sign_with: Turnkey signing identity (wallet account address / private key address / private key ID)
            turnkey_client: Optional Turnkey client instance, will create if not provided
        """
        self.sign_with = sign_with
        self._turnkey = turnkey_client
        self._cached_address: Optional[str] = None

    def _get_turnkey_client(self):
        """Lazy initialization of Turnkey client."""
        if self._turnkey is None:
            try:
                from spoon_ai.turnkey import Turnkey
                self._turnkey = Turnkey()
            except Exception as e:
                raise SignerError(f"Failed to initialize Turnkey client: {str(e)}")
        return self._turnkey

    async def sign_transaction(self, tx_dict: Dict[str, Any], rpc_url: str) -> str:
        """Sign transaction using Turnkey API."""
        try:
            # Convert transaction dict to raw hex using web3
            from web3 import Web3
            w3 = Web3()

            # Create unsigned transaction and serialize to hex
            unsigned_tx = w3.eth.account.sign_transaction(tx_dict, "")  # Empty key to get unsigned tx
            raw_tx_hex = "0x" + unsigned_tx.raw_transaction.hex()

            # Sign via Turnkey
            client = self._get_turnkey_client()
            response = client.sign_evm_transaction(self.sign_with, raw_tx_hex)

            # Extract signed transaction from response
            if "activity" in response and "result" in response["activity"]:
                result = response["activity"]["result"]
                if "signTransactionResult" in result:
                    return result["signTransactionResult"]["signedTransaction"]
                elif "signTransactionResultV2" in result:
                    return result["signTransactionResultV2"]["signedTransaction"]

            raise SignerError("Invalid Turnkey response structure")

        except Exception as e:
            raise SignerError(f"Turnkey signing failed: {str(e)}")

    async def get_address(self) -> str:
        """Get the signing address."""
        if self._cached_address is None:
            # Try to extract address from sign_with if it's an address
            if self.sign_with.startswith("0x") and len(self.sign_with) == 42:
                self._cached_address = self.sign_with
            else:
                # For wallet/private key IDs, we might need to query Turnkey
                # For now, raise an error as we need the address explicitly
                raise SignerError("Turnkey signer requires explicit address for get_address()")
        return self._cached_address

    @property
    def signer_type(self) -> str:
        return "turnkey"


class SignerManager:
    """Manager for creating and configuring signers."""

    @staticmethod
    def create_signer(
        signer_type: str = "auto",
        private_key: Optional[str] = None,
        turnkey_sign_with: Optional[str] = None,
        turnkey_address: Optional[str] = None
    ) -> EvmSigner:
        """
        Create a signer based on configuration.

        Args:
            signer_type: 'local', 'turnkey', or 'auto'
            private_key: Private key for local signing
            turnkey_sign_with: Turnkey signing identity
            turnkey_address: Turnkey signer address (for address resolution)

        Returns:
            Configured signer instance
        """
        # Auto-detect signer type
        if signer_type == "auto":
            if turnkey_sign_with:
                signer_type = "turnkey"
            elif private_key:
                signer_type = "local"
            else:
                # Check environment variables
                if os.getenv("TURNKEY_SIGN_WITH"):
                    signer_type = "turnkey"
                elif os.getenv("EVM_PRIVATE_KEY"):
                    signer_type = "local"
                else:
                    raise ValueError("Cannot auto-detect signer type, please specify signer_type or provide credentials")

        if signer_type == "local":
            key = private_key or os.getenv("EVM_PRIVATE_KEY")
            if not key:
                raise ValueError("Private key required for local signing")
            return LocalSigner(key)

        elif signer_type == "turnkey":
            sign_with = turnkey_sign_with or os.getenv("TURNKEY_SIGN_WITH")
            if not sign_with:
                raise ValueError("turnkey_sign_with required for Turnkey signing")

            signer = TurnkeySigner(sign_with)
            if turnkey_address:
                signer._cached_address = turnkey_address
            elif os.getenv("TURNKEY_ADDRESS"):
                signer._cached_address = os.getenv("TURNKEY_ADDRESS")

            return signer

        else:
            raise ValueError(f"Unknown signer type: {signer_type}")


# Global signer instance for convenience
_default_signer: Optional[EvmSigner] = None

def get_default_signer() -> EvmSigner:
    """Get the default signer instance."""
    global _default_signer
    if _default_signer is None:
        _default_signer = SignerManager.create_signer()
    return _default_signer

def set_default_signer(signer: EvmSigner):
    """Set the default signer instance."""
    global _default_signer
    _default_signer = signer
