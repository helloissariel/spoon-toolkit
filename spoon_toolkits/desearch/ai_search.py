from fastmcp import FastMCP
from .cache import time_cache
from .http_client import desearch_client
from typing import Dict, Any, List

mcp = FastMCP("AISearch")

@mcp.tool()
@time_cache()
async def search_ai_data(query: str, platforms: str = "x,reddit,arxiv,wikipedia,youtube", limit: int = 10) -> Dict[str, Any]:
    """
    Search for AI-related data across multiple platforms using Desearch API.
    
    Args:
        query: Search query string
        platforms: Comma-separated list of platforms (x,reddit,arxiv,wikipedia,youtube)
        limit: Maximum number of results per platform
    
    Returns:
        Dictionary containing search results from all platforms
    """
    platform_list = [p.strip() for p in platforms.split(",")]
    results = {}
    
    for platform in platform_list:
        try:
            endpoint = f"/search/{platform}"
            params = {
                "q": query,
                "limit": limit
            }
            
            response = await desearch_client.get(endpoint, params=params)
            results[platform] = response.json()
        except Exception as e:
            results[platform] = {"error": str(e)}
    
    return {
        "query": query,
        "platforms": platform_list,
        "results": results,
        "total_results": len(results)
    }

@mcp.tool()
@time_cache()
async def search_social_media(query: str, platform: str = "x", limit: int = 10) -> Dict[str, Any]:
    """
    Search social media platforms for real-time information.
    
    Args:
        query: Search query string
        platform: Platform to search (x, reddit)
        limit: Maximum number of results
    
    Returns:
        Dictionary containing social media search results
    """
    try:
        endpoint = f"/search/{platform}"
        params = {
            "q": query,
            "limit": limit
        }
        
        response = await desearch_client.get(endpoint, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
@time_cache()
async def search_academic(query: str, platform: str = "arxiv", limit: int = 10) -> Dict[str, Any]:
    """
    Search academic platforms for research papers and scholarly content.
    
    Args:
        query: Search query string
        platform: Platform to search (arxiv, wikipedia)
        limit: Maximum number of results
    
    Returns:
        Dictionary containing academic search results
    """
    try:
        endpoint = f"/search/{platform}"
        params = {
            "q": query,
            "limit": limit
        }
        
        response = await desearch_client.get(endpoint, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)} 