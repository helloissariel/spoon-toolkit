from fastmcp import FastMCP
from .cache import time_cache
from .http_client import desearch_client
from typing import Dict, Any, List

mcp = FastMCP("DataVerification")

@mcp.tool()
@time_cache()
async def verify_claim(claim: str, sources: str = "x,reddit,wikipedia,news") -> Dict[str, Any]:
    """
    Verify a claim across multiple sources using Desearch API.
    
    Args:
        claim: The claim to verify
        sources: Comma-separated list of sources to check
    
    Returns:
        Dictionary containing verification results and credibility score
    """
    source_list = [s.strip() for s in sources.split(",")]
    verification_results = {}
    credibility_score = 0
    total_sources = len(source_list)
    
    for source in source_list:
        try:
            endpoint = f"/verify/{source}"
            data = {
                "claim": claim
            }
            
            response = await desearch_client.post(endpoint, json=data)
            source_result = response.json()
            verification_results[source] = source_result
            
            # Calculate credibility score
            if source_result.get("verified", False):
                credibility_score += 1
        except Exception as e:
            verification_results[source] = {"error": str(e)}
    
    # Calculate final credibility score
    final_score = (credibility_score / total_sources) * 100 if total_sources > 0 else 0
    
    return {
        "claim": claim,
        "sources": source_list,
        "verification_results": verification_results,
        "credibility_score": final_score,
        "verified_sources": credibility_score,
        "total_sources": total_sources
    }

@mcp.tool()
@time_cache()
async def check_fact_accuracy(fact: str) -> Dict[str, Any]:
    """
    Check the accuracy of a factual statement.
    
    Args:
        fact: The factual statement to verify
    
    Returns:
        Dictionary containing accuracy assessment
    """
    return await verify_claim(claim=fact, sources="wikipedia,news,academic")

@mcp.tool()
@time_cache()
async def detect_misinformation(content: str) -> Dict[str, Any]:
    """
    Detect potential misinformation in content.
    
    Args:
        content: Content to analyze for misinformation
    
    Returns:
        Dictionary containing misinformation analysis
    """
    return await verify_claim(claim=content, sources="x,reddit,news,fact_check") 