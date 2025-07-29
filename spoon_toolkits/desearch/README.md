# Desearch AI Integration for Spoon Toolkit

This module provides AI-powered search and metadata extraction capabilities for the Spoon framework, enabling real-time, verifiable access to open web data.

## 🚀 Features

### Phase 1: AI Data Source Toolset (Current)
- **Multi-platform Search**: Search across X, Reddit, ArXiv, Wikipedia, YouTube
- **Data Verification**: Cross-platform validation and credibility scoring
- **Multi-source Aggregation**: Aggregate and analyze data from multiple sources
- **Real-time Access**: Get real-time, verifiable data to solve AI hallucinations

### Phase 2: Metadata Extraction Engine *(TODO)*
- Structured information extraction
- Multi-platform data parsing
- Metadata standardization

### Phase 3: Trend Analysis Tool *(TODO)*
- Market trend analysis
- Social trend insights
- Prediction model integration

## 📦 Installation

### 1. Install Dependencies
```bash
pip install aiohttp>=3.8.0
pip install fastmcp>=0.1.0
pip install python-dotenv>=1.0.0
```

### 2. Configure Environment Variables
Create a `.env` file in your project root:
```bash
# Desearch API Configuration
DESEARCH_API_KEY=your_api_key_here
DESEARCH_BASE_URL=https://apis.desearch.ai
DESEARCH_TIMEOUT=30
DESEARCH_RETRY_COUNT=3
DESEARCH_CACHE_TTL=300
DESEARCH_RATE_LIMIT=100
DESEARCH_LOG_LEVEL=INFO
```

## 🛠️ Usage

### Basic Usage

```python
from spoon_toolkits.desearch import AISearchTool, DataVerificationTool, MultiSourceSearchTool

# Initialize tools
ai_search = AISearchTool()
verification = DataVerificationTool()
multi_search = MultiSourceSearchTool()

# Search across multiple platforms
results = await ai_search.execute(
    query="AI developments 2024",
    platforms=["x", "reddit", "arxiv"],
    limit=10
)

# Verify a claim
verification_result = await verification.execute(
    claim="OpenAI released GPT-5",
    sources=["x", "reddit", "wikipedia", "news"]
)

# Aggregate data from multiple sources
aggregated = await multi_search.execute(
    query="cryptocurrency trends",
    sources=["x", "reddit", "wikipedia", "news", "youtube"]
)
```

### MCP Tools

The module provides several MCP tools for easy integration:

#### AI Search Tools
- `search_ai_data()`: Search across multiple platforms
- `search_social_media()`: Search social media platforms
- `search_academic()`: Search academic platforms

#### Data Verification Tools
- `verify_claim()`: Verify claims across multiple sources
- `check_fact_accuracy()`: Check factual statement accuracy
- `detect_misinformation()`: Detect potential misinformation

#### Multi-source Tools
- `aggregate_search_results()`: Aggregate results from multiple sources
- `cross_platform_analysis()`: Perform cross-platform analysis
- `check_information_consistency()`: Check information consistency

## 🧪 Testing

Run the basic tests:
```bash
cd spoon_toolkits/desearch
python simple_test.py
```

## 📁 Module Structure

```
spoon_toolkits/desearch/
├── __init__.py                    # Module initialization and exports
├── base.py                        # Base tool class
├── http_client.py                 # HTTP client wrapper
├── env.py                         # Environment configuration
├── cache.py                       # Cache decorator
├── ai_search.py                   # AI search tools
├── data_verification.py           # Data verification tools
├── multi_source_search.py         # Multi-source search tools
├── simple_test.py                 # Basic tests
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DESEARCH_API_KEY` | Required | Your Desearch API key |
| `DESEARCH_BASE_URL` | `https://apis.desearch.ai` | API base URL |
| `DESEARCH_TIMEOUT` | `30` | Request timeout in seconds |
| `DESEARCH_RETRY_COUNT` | `3` | Number of retry attempts |
| `DESEARCH_CACHE_TTL` | `300` | Cache time-to-live in seconds |
| `DESEARCH_RATE_LIMIT` | `100` | Rate limit requests per minute |
| `DESEARCH_LOG_LEVEL` | `INFO` | Logging level |

## 🎯 Success Metrics

### Phase 1 Goals
- ✅ Multi-platform search functionality
- ✅ Data verification capabilities
- ✅ Multi-source aggregation
- ✅ Real-time data access
- ✅ Credibility scoring
- ✅ Consistency analysis

## 🤝 Contributing

This module follows the existing Spoon Toolkit patterns and conventions. When contributing:

1. Follow the existing code style (PascalCase for classes, snake_case for functions)
2. Use async/await for all I/O operations
3. Implement proper error handling
4. Add appropriate caching with `@time_cache()`
5. Include comprehensive tests

## 📄 License

This module is part of the Spoon Toolkit project and follows the same license terms. 