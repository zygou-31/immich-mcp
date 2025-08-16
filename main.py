from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import httpx
import logging
import contextlib
from contextlib import asynccontextmanager

from immich_mcp.client import ImmichClient
from immich_mcp.config import ImmichConfig, load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Global variable for config
config: ImmichConfig = None
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """
    global config
    try:
        config = load_config()
        app.state.config = config
        logger.info("Configuration loaded successfully")
        if not await config.test_connection():
            raise ValueError("Immich API connection test failed.")

        # Create and attach the Immich client
        immich_client = ImmichClient(config)
        app.state.immich_client = immich_client

        # Create and attach the tools
        immich_tools = ImmichTools(immich_client)
        app.state.immich_tools = immich_tools

        # Create and mount the tool server
        tool_server = ToolServer(
            name="immich-mcp-server",
            instructions="MCP server for Immich API with tools for pinging, albums, assets, search, and uploads.",
            tools=[
                Tool.from_function(immich_tools.ping_server),
                Tool.from_function(immich_tools.get_all_albums),
                Tool.from_function(immich_tools.get_asset_info),
                Tool.from_function(immich_tools.search_photos),
                Tool.from_function(immich_tools.upload_photo),
                Tool.from_function(immich_tools.create_album),
            ],
        )
        app.mount("/mcp", tool_server.streamable_http_app())

        async with contextlib.AsyncExitStack() as stack:
            await stack.enter_async_context(tool_server.session_manager.run())
            yield
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise


# Security scheme
auth_scheme = HTTPBearer()


# Dependency to verify the token
def verify_token(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    config = request.app.state.config
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != config.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


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


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        lifespan=lifespan,
    )
    router = APIRouter()
    router.add_api_route(
        "/", lambda: {"message": "Hello World"}, dependencies=[Depends(verify_token)]
    )
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8626)
