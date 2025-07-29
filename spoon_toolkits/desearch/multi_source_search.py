from fastmcp import FastMCP
from .cache import time_cache
from .http_client import desearch_client
from typing import Dict, Any, List

mcp = FastMCP("MultiSourceSearch")

@mcp.tool()
@time_cache()
async def aggregate_search_results(query: str, sources: str = "x,reddit,wikipedia,news,youtube") -> Dict[str, Any]:
    """
    Aggregate search results from multiple sources.
    
    Args:
        query: Search query
        sources: Comma-separated list of sources
    
    Returns:
        Dictionary containing aggregated results and consistency analysis
    """
    source_list = [s.strip() for s in sources.split(",")]
    source_results = {}
    aggregated_data = []
    
    for source in source_list:
        try:
            endpoint = f"/search/{source}"
            params = {
                "q": query,
                "limit": 20
            }
            
            response = await desearch_client.get(endpoint, params=params)
            source_result = response.json()
            source_results[source] = source_result
            
            if "results" in source_result:
                aggregated_data.extend(source_result["results"])
        except Exception as e:
            source_results[source] = {"error": str(e)}
    
    # Perform consistency analysis
    consistency_analysis = await _analyze_consistency(aggregated_data)
    
    return {
        "query": query,
        "sources": source_list,
        "source_results": source_results,
        "aggregated_data": aggregated_data,
        "consistency_analysis": consistency_analysis,
        "total_results": len(aggregated_data)
    }

@mcp.tool()
@time_cache()
async def cross_platform_analysis(topic: str) -> Dict[str, Any]:
    """
    Perform cross-platform analysis on a specific topic.
    
    Args:
        topic: Topic to analyze across platforms
    
    Returns:
        Dictionary containing cross-platform analysis results
    """
    return await aggregate_search_results(query=topic, sources="x,reddit,wikipedia,news")

@mcp.tool()
@time_cache()
async def check_information_consistency(claim: str) -> Dict[str, Any]:
    """
    Check consistency of information across multiple sources.
    
    Args:
        claim: Claim to check for consistency
    
    Returns:
        Dictionary containing consistency analysis
    """
    return await aggregate_search_results(query=claim, sources="wikipedia,news,academic")

async def _analyze_consistency(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze consistency across aggregated data"""
    if not data:
        return {"consistency_score": 0, "conflicts": [], "agreements": []}
    
    # Simple consistency analysis
    # In a real implementation, this would use more sophisticated NLP
    consistency_score = 0
    conflicts = []
    agreements = []
    
    # For now, return a basic structure
    return {
        "consistency_score": consistency_score,
        "conflicts": conflicts,
        "agreements": agreements,
        "total_items": len(data)
    } 