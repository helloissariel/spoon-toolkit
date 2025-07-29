# Desearch AI Integration

A powerful search and verification toolkit for the Spoon framework that provides real-time access to verified data across multiple platforms. This module helps solve AI hallucination problems by aggregating and cross-validating information from trusted sources.

## What It Does

The Desearch integration enables AI agents to search and verify information across:
- **Social Media**: X (Twitter), Reddit
- **Academic Sources**: ArXiv, Wikipedia
- **Video Platforms**: YouTube
- **News Sources**: Real-time news aggregation

Instead of relying on potentially outdated or hallucinated data, your AI agents can now access current, verified information from multiple sources simultaneously.

## Quick Start

### Prerequisites

You'll need a Desearch API key. Contact the Desearch team or visit their documentation to get one.

### Installation

1. **Install dependencies**:
```bash
pip install httpx>=0.28.0
pip install fastmcp>=0.1.0
pip install python-dotenv>=1.0.0
```

2. **Set up environment variables**:
Create a `.env` file in your project root:
```bash
DESEARCH_API_KEY=your_actual_api_key_here
DESEARCH_BASE_URL=https://apis.desearch.ai
DESEARCH_TIMEOUT=30
```

### Basic Usage

```python
from spoon_toolkits.desearch import search_ai_data, verify_claim

# Search for current AI developments
results = await search_ai_data(
    query="latest AI developments 2024",
    platforms="x,reddit,arxiv",
    limit=10
)

# Verify a claim about a new product launch
verification = await verify_claim(
    claim="OpenAI released GPT-5",
    sources="x,reddit,wikipedia,news"
)
```

## Available Tools

### Search Tools

#### `search_ai_data(query, platforms, limit)`
Searches across multiple platforms simultaneously.

**Parameters:**
- `query` (str): Your search term
- `platforms` (str): Comma-separated list: "x,reddit,arxiv,wikipedia,youtube"
- `limit` (int): Max results per platform (default: 10)

**Returns:**
```json
{
  "query": "AI developments",
  "platforms": ["x", "reddit", "arxiv"],
  "results": {
    "x": [...],
    "reddit": [...],
    "arxiv": [...]
  },
  "total_results": 3
}
```

#### `search_social_media(query, platform, limit)`
Focused search on social media platforms.

**Example:**
```python
# Search X for cryptocurrency discussions
results = await search_social_media(
    query="bitcoin price analysis",
    platform="x",
    limit=20
)
```

#### `search_academic(query, platform, limit)`
Search academic and research sources.

**Example:**
```python
# Find recent AI research papers
papers = await search_academic(
    query="large language models",
    platform="arxiv",
    limit=15
)
```

### Verification Tools

#### `verify_claim(claim, sources)`
Cross-validates a claim across multiple sources.

**Parameters:**
- `claim` (str): The statement to verify
- `sources` (str): Sources to check: "x,reddit,wikipedia,news"

**Returns:**
```json
{
  "claim": "OpenAI released GPT-5",
  "sources": ["x", "reddit", "wikipedia", "news"],
  "verification_results": {...},
  "credibility_score": 75.0,
  "verified_sources": 3,
  "total_sources": 4
}
```

#### `check_fact_accuracy(fact)`
Specialized tool for factual statements.

#### `detect_misinformation(content)`
Analyzes content for potential misinformation.

### Aggregation Tools

#### `aggregate_search_results(query, sources)`
Combines results from multiple sources with consistency analysis.

#### `cross_platform_analysis(topic)`
Performs comprehensive analysis across platforms.

#### `check_information_consistency(claim)`
Checks information consistency across academic and news sources.

## Real-World Examples

### Example 1: Market Research
```python
# Research cryptocurrency market sentiment
market_data = await search_ai_data(
    query="bitcoin ethereum market sentiment",
    platforms="x,reddit,news",
    limit=15
)

# Verify a market claim
verification = await verify_claim(
    claim="Bitcoin reached new all-time high",
    sources="x,reddit,news"
)
```

### Example 2: Academic Research
```python
# Find recent papers on a topic
papers = await search_academic(
    query="quantum computing applications",
    platform="arxiv",
    limit=20
)

# Cross-validate research findings
consistency = await check_information_consistency(
    "Quantum computers can break RSA encryption"
)
```

### Example 3: News Verification
```python
# Check if a news story is accurate
accuracy = await check_fact_accuracy(
    "Tesla announced new electric vehicle model"
)

# Detect potential misinformation
misinfo_check = await detect_misinformation(
    "Vaccines cause autism"  # This would be flagged
)
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DESEARCH_API_KEY` | Yes | - | Your API key from Desearch |
| `DESEARCH_BASE_URL` | No | `https://apis.desearch.ai` | API endpoint |
| `DESEARCH_TIMEOUT` | No | `30` | Request timeout (seconds) |
| `DESEARCH_RETRY_COUNT` | No | `3` | Retry attempts |
| `DESEARCH_CACHE_TTL` | No | `300` | Cache duration (seconds) |
| `DESEARCH_RATE_LIMIT` | No | `100` | Requests per minute |
| `DESEARCH_LOG_LEVEL` | No | `INFO` | Logging level |

### Advanced Configuration

For production deployments, consider these settings:

```bash
# Production settings
DESEARCH_TIMEOUT=60
DESEARCH_RETRY_COUNT=5
DESEARCH_CACHE_TTL=600
DESEARCH_RATE_LIMIT=50
DESEARCH_LOG_LEVEL=WARNING
```

## Testing

Run the basic functionality test:

```bash
cd spoon_toolkits/desearch
python simple_test.py
```

Expected output:
```
🧪 Running simple tests for Desearch AI integration...

✓ API Key configured: Yes
✓ Base URL: https://apis.desearch.ai
✓ Environment configuration test passed
✓ Desearch HTTP client initialized successfully
✓ HTTP client test passed

✅ Simple tests completed!
```

## Troubleshooting

### Common Issues

#### 1. "API Key not configured"
**Problem**: `DESEARCH_API_KEY` environment variable is not set.

**Solution**: 
```bash
export DESEARCH_API_KEY=your_key_here
# Or add to .env file
echo "DESEARCH_API_KEY=your_key_here" >> .env
```

#### 2. "HTTP request failed"
**Problem**: Network issues or API endpoint problems.

**Solutions**:
- Check your internet connection
- Verify the API key is valid
- Try increasing `DESEARCH_TIMEOUT`
- Check if the Desearch service is operational

#### 3. "No results returned"
**Problem**: Search queries returning empty results.

**Solutions**:
- Try different keywords
- Check if the platforms are available
- Verify the query format
- Try reducing the `limit` parameter

#### 4. "Rate limit exceeded"
**Problem**: Too many requests in a short time.

**Solutions**:
- Reduce `DESEARCH_RATE_LIMIT`
- Implement request throttling
- Use caching more aggressively

### Debug Mode

Enable detailed logging:

```bash
export DESEARCH_LOG_LEVEL=DEBUG
```

### Performance Tips

1. **Use caching**: All functions are cached by default (5 minutes)
2. **Batch requests**: Use `aggregate_search_results` for multiple sources
3. **Optimize queries**: Be specific with search terms
4. **Monitor rate limits**: Stay within API limits

## Module Structure

```
spoon_toolkits/desearch/
├── __init__.py              # Module exports and MCP server
├── ai_search.py             # Search functionality
├── data_verification.py     # Verification tools
├── multi_source_search.py   # Aggregation tools
├── http_client.py           # HTTP client (httpx)
├── env.py                   # Environment configuration
├── cache.py                 # Caching decorator
├── simple_test.py           # Basic tests
└── README.md               # This file
```

## Integration with Spoon Framework

This module integrates seamlessly with the Spoon framework:

```python
from spoon_toolkits.desearch import search_ai_data

# Use in your AI agent
class MyAgent:
    async def research_topic(self, topic):
        results = await search_ai_data(
            query=topic,
            platforms="x,reddit,arxiv",
            limit=10
        )
        return self.analyze_results(results)
```

## Contributing

When contributing to this module:

1. **Follow existing patterns**: Use the same code style as other Spoon modules
2. **Add tests**: Include tests for new functionality
3. **Update docs**: Keep this README current
4. **Use async/await**: All I/O operations should be async
5. **Handle errors gracefully**: Return error info instead of raising exceptions

## License

This module is part of the Spoon Toolkit project and follows the same license terms.

## Support

For issues with this module:
1. Check the troubleshooting section above
2. Review the Spoon Toolkit documentation
3. Contact the development team

For Desearch API issues:
- Check the Desearch API documentation
- Contact Desearch support team 