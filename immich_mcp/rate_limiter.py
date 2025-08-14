"""
Rate limiting module for Immich MCP server to prevent API abuse.
"""

import asyncio
import time
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Token bucket rate limiter for API requests."""

    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window  # seconds
        self.requests: Dict[str, list] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, client_id: str = "default") -> bool:
        """Acquire permission to make a request."""
        async with self._lock:
            now = time.time()

            # Initialize client if not exists
            if client_id not in self.requests:
                self.requests[client_id] = []

            # Remove old requests outside the window
            self.requests[client_id] = [
                req_time
                for req_time in self.requests[client_id]
                if now - req_time < self.window
            ]

            # Check if under limit
            if len(self.requests[client_id]) < self.max_requests:
                self.requests[client_id].append(now)
                return True
            else:
                logger.warning(f"Rate limit exceeded for client {client_id}")
                return False

    async def wait_for_slot(self, client_id: str = "default") -> None:
        """Wait until a rate limit slot is available."""
        while not await self.acquire(client_id):
            await asyncio.sleep(1)
