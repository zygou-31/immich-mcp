

import os
from typing import List, Optional, Any

import httpx
from pydantic import BaseModel, HttpUrl, Field

# --- Pydantic Models for Immich API Responses ---

class ServerInfoResponse(BaseModel):
    version: str
    isReady: bool
    userName: str
    admin: bool
    url: HttpUrl
    loginPageMessage: Optional[str] = None
    externalUrl: Optional[HttpUrl] = None
    disableAdmin: bool
    liveSyncEnabled: bool
    trashDays: int
    isAllowUpload: bool = Field(..., alias="is_allow_upload")

class SmartSearchResponse(BaseModel):
    id: str

class AssetResponse(BaseModel):
    id: str
    createdAt: str
    updatedAt: str
    deletedAt: Optional[str] = None
    userId: str
    checksum: str
    originalPath: str
    originalProperties: dict
    deviceAssetId: str
    deviceId: str
    type: str # 'IMAGE', 'VIDEO'
    mimeType: str
    duration: Optional[str] = None
    fileCreatedAt: str
    fileModifiedAt: str
    webpPath: Optional[str] = None
    encodedVideoPath: Optional[str] = None
    livePhotoVideoId: Optional[str] = None
    isFavorite: bool
    isArchived: bool
    isTrash: bool
    isExternal: bool
    isReadOnly: bool
    isOffline: bool
    webpHash: Optional[str] = None
    motionVectorPath: Optional[str] = None
    sidecarPath: Optional[str] = None
    stackParentId: Optional[str] = None
    stackCount: Optional[int] = None

class AlbumResponse(BaseModel):
    id: str
    ownerId: str
    albumName: str
    createdAt: str
    updatedAt: str
    shared: bool
    albumThumbnailAssetId: Optional[str] = None
    assetCount: int
    assets: List[AssetResponse] = []

# --- ImmichClient Class ---

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

    async def _request(self, method: str, path: str, **kwargs):
        try:
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            raise

    async def ping(self) -> ServerInfoResponse:
        """Health check and server info."""
        data = await self._request("GET", "api/server-info/ping")
        return ServerInfoResponse(**data)

    async def search_smart(self, query: str, limit: int = 20) -> List[SmartSearchResponse]:
        """Perform a smart search for assets."""
        params = {"q": query, "limit": limit}
        data = await self._request("GET", "api/search/smart", params=params)
        return [SmartSearchResponse(**item) for item in data]

    async def upload_asset(self, file_path: str) -> AssetResponse:
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

        json_response = await self._request("POST", "api/asset/upload", files=files, data=data) 
        
        # Close the file after upload
        files["assetData"][1].close()

        # The Immich upload endpoint usually returns an UploadResponse, but we'll adapt to AssetResponse
        # For a full implementation, you might need a dedicated UploadResponse model
        return AssetResponse(**json_response)

    async def list_albums(self) -> List[AlbumResponse]:
        """List all albums."""
        data = await self._request("GET", "api/albums")
        return [AlbumResponse(**item) for item in data]

    async def get_asset_details(self, asset_id: str) -> AssetResponse:
        """Get details for a specific asset by ID."""
        data = await self._request("GET", f"api/assets/{asset_id}")
        return AssetResponse(**data)

