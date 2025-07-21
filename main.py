
from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI
from dotenv import load_dotenv
import os

from immich_mcp.client import ImmichClient

load_dotenv()

app = FastAPI()

import httpx

class ImmichTools:
    def __init__(self):
        self.immich_api_key = os.getenv("IMMICH_API_KEY")
        self.immich_base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283/api")
        self.client = ImmichClient(base_url=self.immich_base_url, api_key=self.immich_api_key)

    async def ping_server(self) -> str:
        """Pings the Immich server to check for a connection."""
        try:
            response = await self.client.ping()
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error pinging server: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error pinging server: {e}"

    async def get_all_albums(self) -> str:
        """Retrieves all albums from Immich."""
        try:
            response = await self.client.list_albums()
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error getting albums: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error getting albums: {e}"

    async def get_asset_info(self, asset_id: str) -> str:
        """Retrieves information about a specific asset."""
        try:
            response = await self.client.get_asset_details(asset_id)
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error getting asset info: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error getting asset info: {e}"

    async def search_photos(self, query: str, limit: int = 20, album_id: str = None) -> str:
        """Searches for photos in Immich."""
        try:
            response = await self.client.search_smart(query, limit, album_id)
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error searching photos: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error searching photos: {e}"

    async def upload_photo(self, file_path: str, album_id: str = None) -> str:
        """Uploads a photo to Immich."""
        try:
            response = await self.client.upload_asset(file_path, album_id)
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error uploading photo: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error uploading photo: {e}"
        except FileNotFoundError as e:
            return str(e)
            
    async def create_album(self, album_name: str, description: str = "", assets: list = []) -> str:
        """Creates a new album in Immich."""
        try:
            response = await self.client.create_album(album_name, description, assets)
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error creating album: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error creating album: {e}"


tool_server = ToolServer(
    name="immich-mcp-server",
    instructions="MCP server for Immich API with tools for pinging, albums, assets, search, and uploads.",
    version="0.1.0",
    tools=[
        Tool.from_function(ImmichTools().ping_server),
        Tool.from_function(ImmichTools().get_all_albums),
        Tool.from_function(ImmichTools().get_asset_info),
        Tool.from_function(ImmichTools().search_photos),
        Tool.from_function(ImmichTools().upload_photo),
        Tool.from_function(ImmichTools().create_album),
    ],
)

# FastMCP creates its own Starlette app; mount it to FastAPI
app.mount("/", tool_server.streamable_http_app()) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
