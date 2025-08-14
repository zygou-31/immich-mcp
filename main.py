from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import httpx

from immich_mcp.client import ImmichClient

from immich_mcp.config import ImmichConfig
import asyncio

load_dotenv()

app = FastAPI()

# Load configuration and test connection on startup
try:
    print("Loaded environment variables:")
    print(f"  IMMICH_BASE_URL: {os.getenv('IMMICH_BASE_URL')}")
    print(f"  IMMICH_API_KEY: {os.getenv('IMMICH_API_KEY')}")
    print(f"  IMMICH_TIMEOUT: {os.getenv('IMMICH_TIMEOUT')}")
    print(f"  IMMICH_MAX_RETRIES: {os.getenv('IMMICH_MAX_RETRIES')}")
    config = ImmichConfig(
        base_url=os.getenv("IMMICH_BASE_URL"),
        api_key=os.getenv("IMMICH_API_KEY"),
        timeout=int(os.getenv("IMMICH_TIMEOUT", 30)),
        max_retries=int(os.getenv("IMMICH_MAX_RETRIES", 3)),
    )
    if not asyncio.run(config.test_connection()):
        raise ValueError("Immich API connection test failed.")
except Exception as e:
    print(f"Configuration error: {e}")
    exit(1)

# Create a single ImmichClient instance
immich_client = ImmichClient(config)


class ImmichTools:
    def __init__(self, client: ImmichClient):
        self.client = client

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

    async def search_photos(
        self, query: str, limit: int = 20, album_id: str = None
    ) -> str:
        """Searches for photos in Immich."""
        try:
            response = await self.client.search_smart(query, limit, album_id)
            return response.json()
        except httpx.HTTPStatusError as e:
            return (
                f"Error searching photos: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            return f"Network error searching photos: {e}"

    async def upload_photo(self, file_path: str, album_id: str = None) -> str:
        """Uploads a photo to Immich."""
        try:
            response = await self.client.upload_asset(file_path, album_id)
            return response.json()
        except httpx.HTTPStatusError as e:
            return (
                f"Error uploading photo: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            return f"Network error uploading photo: {e}"
        except FileNotFoundError as e:
            return str(e)

    async def create_album(
        self, album_name: str, description: str = "", assets: list = []
    ) -> str:
        """Creates a new album in Immich."""
        try:
            response = await self.client.create_album(album_name, description, assets)
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"Error creating album: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error creating album: {e}"


# Create an instance of ImmichTools with the shared client
immich_tools = ImmichTools(immich_client)

tool_server = ToolServer(
    name="immich-mcp-server",
    instructions="MCP server for Immich API with tools for pinging, albums, assets, search, and uploads.",
    version="0.1.0",
    tools=[
        Tool.from_function(immich_tools.ping_server),
        Tool.from_function(immich_tools.get_all_albums),
        Tool.from_function(immich_tools.get_asset_info),
        Tool.from_function(immich_tools.search_photos),
        Tool.from_function(immich_tools.upload_photo),
        Tool.from_function(immich_tools.create_album),
    ],
)

# FastMCP creates its own Starlette app; mount it to FastAPI
app.mount("/", tool_server.streamable_http_app())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
