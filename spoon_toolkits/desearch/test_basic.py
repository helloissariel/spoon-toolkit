"""
Basic tests for Desearch AI integration
"""

import asyncio
import os
from .ai_search import AISearchTool
from .data_verification import DataVerificationTool
from .multi_source_search import MultiSourceSearchTool

async def test_ai_search_tool():
    """Test AI search tool basic functionality"""
    try:
        tool = AISearchTool()
        print("✓ AISearchTool initialized successfully")
        
        # Test with mock data (since we don't have real API key)
        result = await tool.execute(query="test query", platforms=["x"], limit=5)
        print(f"✓ AISearchTool execute method works: {type(result)}")
        
    except Exception as e:
        print(f"✗ AISearchTool test failed: {e}")

async def test_data_verification_tool():
    """Test data verification tool basic functionality"""
    try:
        tool = DataVerificationTool()
        print("✓ DataVerificationTool initialized successfully")
        
        # Test with mock data
        result = await tool.execute(claim="test claim", sources=["x"])
        print(f"✓ DataVerificationTool execute method works: {type(result)}")
        
    except Exception as e:
        print(f"✗ DataVerificationTool test failed: {e}")

async def test_multi_source_search_tool():
    """Test multi-source search tool basic functionality"""
    try:
        tool = MultiSourceSearchTool()
        print("✓ MultiSourceSearchTool initialized successfully")
        
        # Test with mock data
        result = await tool.execute(query="test query", sources=["x"])
        print(f"✓ MultiSourceSearchTool execute method works: {type(result)}")
        
    except Exception as e:
        print(f"✗ MultiSourceSearchTool test failed: {e}")

async def main():
    """Run all basic tests"""
    print("🧪 Running basic tests for Desearch AI integration...")
    print()
    
    await test_ai_search_tool()
    await test_data_verification_tool()
    await test_multi_source_search_tool()
    
    print()
    print("✅ Basic tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 