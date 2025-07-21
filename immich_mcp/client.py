import os
import httpx

class ImmichClient:

    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=timeout)

    async def ping(self) -> httpx.Response:
        """Health check and server info."""
        return await self.client.get("api/server-info/ping")

    async def search_smart(self, query: str, limit: int = 20, album_id: str = None) -> httpx.Response:
        """Perform a smart search for assets."""
        params = {"q": query, "limit": limit}
        if album_id:
            params["albumId"] = album_id
        return await self.client.get("api/search/smart", params=params)

    async def upload_asset(self, file_path: str, album_id: str = None) -> httpx.Response:
        """Upload a new asset."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = os.path.basename(file_path)
        
        files = {"assetData": (file_name, open(file_path, "rb"), "application/octet-stream")}
        
        data = {
            "deviceId": "openhands-agent",
            "deviceAssetId": f"{file_name}-{os.path.getsize(file_path)}-{os.path.getmtime(file_path)}",
            "fileCreatedAt": "2023-01-01T00:00:00.000Z",
            "fileModifiedAt": "2023-01-01T00:00:00.000Z",
        }
        if album_id:
            data["albumId"] = album_id

        response = await self.client.post("api/asset/upload", files=files, data=data) 
        
        # Close the file after upload
        files["assetData"][1].close()

        return response

    async def list_albums(self) -> httpx.Response:
        """List all albums."""
        return await self.client.get("api/albums")

    async def create_album(self, album_name: str, description: str = "", assets: list = []) -> httpx.Response:
        """Create a new album."""
        payload = {
            "albumName": album_name,
            "description": description,
            "assetIds": assets,
        }
        return await self.client.post("api/albums", json=payload)

    async def get_asset_details(self, asset_id: str) -> httpx.Response:
        """Get details for a specific asset by ID."""
        return await self.client.get(f"api/assets/{asset_id}")

