

from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI, HTTPException
import httpx
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the new configuration system
from immich_mcp.config import load_config

app = FastAPI()

class ImmichTools:
    def __init__(self):
        # Load and validate configuration
        self.config = load_config()
        logger.info("Immich API configuration loaded")

        # Test connection during startup (async context required)
        import asyncio
        if asyncio.run(self.config.test_connection()):
            logger.info("Successfully connected to Immich API")
        else:
            logger.warning("Could not connect to Immich API - functionality may be limited")

        self.http_client = httpx.AsyncClient(
            base_url=str(self.config.immich_base_url),
            headers={"x-api-key": self.config.immich_api_key},
            timeout=self.config.immich_timeout,
        )

    async def get_server_version(self) -> str:
        """
        Retrieves the Immich server version.
        """
        try:
            response = await self.http_client.get("/server-info/version")
            response.raise_for_status()
            return response.json().get("version", "Unknown")
        except httpx.HTTPStatusError as e:
            return f"Error getting server version: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error getting server version: {e}"

tool_server = ToolServer(
    name="immich-mcp-server",
    instructions="MCP server for Immich API", # Changed description to instructions
    version="0.1.0",
    tools=[Tool.from_function(ImmichTools().get_server_version)],
)

# FastMCP creates its own Starlette app; mount it to FastAPI
app.mount("/", tool_server.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

