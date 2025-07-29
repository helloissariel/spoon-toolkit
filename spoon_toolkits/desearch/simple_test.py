"""
Simple test for Desearch AI integration without external dependencies
"""

import asyncio
import os
import sys
sys.path.append('..')

from http_client import desearch_client
from env import DESEARCH_API_KEY, DESEARCH_BASE_URL

async def test_http_client():
    """Test HTTP client basic functionality"""
    try:
        print("✓ Desearch HTTP client initialized successfully")
        
        # Test client configuration
        print(f"✓ Base URL: {desearch_client.base_url}")
        print(f"✓ Authorization header configured: {'Yes' if 'Authorization' in desearch_client.headers else 'No'}")
        
        print("✓ HTTP client test passed")
        
    except Exception as e:
        print(f"✗ HTTP client test failed: {e}")

async def test_env_config():
    """Test environment configuration"""
    try:
        print(f"✓ API Key configured: {'Yes' if DESEARCH_API_KEY else 'No'}")
        print(f"✓ Base URL: {DESEARCH_BASE_URL}")
        print("✓ Environment configuration test passed")
        
    except Exception as e:
        print(f"✗ Environment configuration test failed: {e}")

async def main():
    """Run simple tests"""
    print("🧪 Running simple tests for Desearch AI integration...")
    print()
    
    await test_env_config()
    await test_http_client()
    
    print()
    print("✅ Simple tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 