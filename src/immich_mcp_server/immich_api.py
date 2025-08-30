import os

import httpx


class ImmichAPI:
    """A client for interacting with the Immich API."""

    def __init__(self, api_url: str | None = None, api_key: str | None = None):
        self.api_url = api_url or os.environ.get("IMMICH_API_URL")
        self.api_key = api_key or os.environ.get("IMMICH_API_KEY")

        if not self.api_url:
            raise ValueError(
                "Immich API URL must be provided via argument or IMMICH_API_URL environment variable."
            )
        if not self.api_key:
            raise ValueError(
                "Immich API key must be provided via argument or IMMICH_API_KEY environment variable."
            )

        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "x-api-key": self.api_key,
                "Accept": "application/json",
            },
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Closes the HTTP client."""
        await self._client.aclose()

    async def ping_server(self) -> bool:
        """Pings the Immich server to check for a valid connection."""
        try:
            response = await self._client.get("/server/ping")
            response.raise_for_status()
            return response.json().get("res") == "pong"
        except (httpx.RequestError, httpx.HTTPStatusError):
            return False
