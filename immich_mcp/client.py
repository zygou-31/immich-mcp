import os
import httpx

from .config import ImmichConfig
import asyncio

class ImmichClient:
    def __init__(self, config: ImmichConfig):
        self.config = config
        self.headers = {
            "x-api-key": self.config.api_key.get_secret_value(),
            "Accept": "application/json"
        }
        self.client = httpx.AsyncClient(
            base_url=str(self.config.base_url),
            headers=self.headers,
            timeout=self.config.timeout
        )

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        for attempt in range(self.config.max_retries):
            try:
                response = await self.client.request(method, path, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(1)  # wait before retrying
                else:
                    raise e
        
    async def ping(self) -> httpx.Response:
        """Health check and server info."""
        return await self._request("GET", "api/server-info/ping")

    async def search_smart(self, query: str, limit: int = 20, album_id: str = None) -> httpx.Response:
        """Perform a smart search for assets."""
        params = {"q": query, "limit": limit}
        if album_id:
            params["albumId"] = album_id
        return await self._request("GET", "api/search/smart", params=params)

    async def upload_asset(self, file_path: str, album_id: str = None) -> httpx.Response:
        """Upload a new asset."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            files = {"assetData": (file_name, f, "application/octet-stream")}
            
            data = {
                "deviceId": "openhands-agent",
                "deviceAssetId": f"{file_name}-{os.path.getsize(file_path)}-{os.path.getmtime(file_path)}",
                "fileCreatedAt": "2023-01-01T00:00:00.000Z",
                "fileModifiedAt": "2023-01-01T00:00:00.000Z",
            }
            if album_id:
                data["albumId"] = album_id

            return await self._request("POST", "api/asset/upload", files=files, data=data)

    async def list_albums(self) -> httpx.Response:
        """List all albums."""
        return await self._request("GET", "api/albums")

    async def create_album(self, album_name: str, description: str = "", assets: list = []) -> httpx.Response:
        """Create a new album."""
        payload = {
            "albumName": album_name,
            "description": description,
            "assetIds": assets,
        }
        return await self._request("POST", "api/albums", json=payload)

    async def get_asset_details(self, asset_id: str) -> httpx.Response:
        """Get details for a specific asset by ID."""
        return await self._request("GET", f"api/assets/{asset_id}")

