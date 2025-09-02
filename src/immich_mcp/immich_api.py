import json
import os

import httpx


class ImmichAPI:
    """A client for interacting with the Immich API."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or os.environ.get("IMMICH_BASE_URL")
        self.api_key = api_key or os.environ.get("IMMICH_API_KEY")

        if not self.base_url:
            raise ValueError(
                "Immich base URL must be provided via argument or IMMICH_BASE_URL environment variable."
            )
        if not self.api_key:
            raise ValueError(
                "Immich API key must be provided via argument or IMMICH_API_KEY environment variable."
            )

        # Ensure the base URL does not end with a slash, then append /api
        api_url = f"{self.base_url.rstrip('/')}/api"

        self._client = httpx.AsyncClient(
            base_url=api_url,
            headers={
                "x-api-key": self.api_key,
                "Accept": "application/json",
            },
            timeout=30.0,
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
            data = response.json()
            return bool(data and data.get("res") == "pong")
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError, ValueError):
            return False
        except Exception:
            return False

    async def get_my_user(self) -> dict:
        """Fetches the current user's details."""
        try:
            response = await self._client.get("/users/me")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return {}

    async def get_users_list(self) -> list[dict]:
        """Fetches the list of users."""
        try:
            response = await self._client.get("/users")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return []

    async def get_partners(self) -> list[dict]:
        """Fetches the list of partners."""
        try:
            response = await self._client.get("/partners", params={"direction": "shared-by"})
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return []

    async def get_asset(self, asset_id: str) -> dict:
        """Fetches a single asset by its ID."""
        try:
            response = await self._client.get(f"/assets/{asset_id}")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return {}

    async def get_my_api_key(self) -> dict:
        """Fetches the current API key's details."""
        try:
            response = await self._client.get("/api-keys/me")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return {}

    async def get_api_key_list(self) -> list[dict]:
        """Fetches the list of API keys."""
        try:
            response = await self._client.get("/api-keys")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return []

    async def get_api_key(self, api_key_id: str) -> dict:
        """Fetches a single API key by its ID."""
        try:
            response = await self._client.get(f"/api-keys/{api_key_id}")
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return {}
