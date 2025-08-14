"""
Caching module for Immich MCP server with TTL support and memory management.
"""

import asyncio
import time
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Thread-safe in-memory cache with TTL support."""

    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired."""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if entry["expires"] > time.time():
                    return entry["value"]
                else:
                    # Remove expired entry
                    del self._cache[key]
            return None

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        """Set value in cache with TTL (default 5 minutes)."""
        async with self._lock:
            # Remove oldest entries if cache is full
            if len(self._cache) >= self._max_size:
                oldest_key = min(
                    self._cache.keys(), key=lambda k: self._cache[k]["expires"]
                )
                del self._cache[oldest_key]

            self._cache[key] = {"value": value, "expires": time.time() + ttl}

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()

    async def size(self) -> int:
        """Get current cache size."""
        async with self._lock:
            return len(self._cache)
