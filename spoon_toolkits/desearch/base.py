import os
import logging
from typing import Dict, Any
from spoon_ai.tools.base import BaseTool

logger = logging.getLogger(__name__)

class DesearchBaseTool(BaseTool):
    """Base class for all Desearch tools"""
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("DESEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("DESEARCH_API_KEY is not set in environment variables")
        
        self.base_url = os.getenv("DESEARCH_BASE_URL", "https://apis.desearch.ai")
        self.timeout = int(os.getenv("DESEARCH_TIMEOUT", "30"))
        self.retry_count = int(os.getenv("DESEARCH_RETRY_COUNT", "3"))
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool with error handling"""
        try:
            result = await self._execute_internal(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing {self.name}: {str(e)}")
            return {"error": str(e)}
    
    async def _execute_internal(self, **kwargs) -> Dict[str, Any]:
        """Internal execution method to be implemented by subclasses"""
        raise NotImplementedError 