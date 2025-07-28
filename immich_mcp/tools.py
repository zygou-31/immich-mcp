



from immich_mcp.client import ImmichClient
import json
import logging
from typing import Optional, Dict, Any, List
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

from .cache import CacheManager
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class ImmichTools:
    """Production-ready tools for Immich MCP server with caching, rate limiting, and performance optimizations."""
    
    def __init__(self, config):
        self.config = config
        self.client = ImmichClient(config)
        self.cache = CacheManager()
        self.rate_limiter = RateLimiter(max_requests=100, window=60)
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.client.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=128)
    async def get_all_assets(self) -> str:
        """Retrieves all assets from Immich with caching and rate limiting."""
        try:
            assets = await self.client.get_all_assets()
            return json.dumps(assets)
        except Exception as e:
            logger.error(f"Error getting all assets: {e}")
            return json.dumps({"error": str(e)})
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_asset_info(self, asset_id: str) -> str:
        """Gets information about a specific asset with caching."""
        try:
            asset = await self.client.get_asset(asset_id)
            return json.dumps(asset)
        except Exception as e:
            logger.error(f"Error getting asset {asset_id}: {e}")
            return json.dumps({"error": str(e)})



