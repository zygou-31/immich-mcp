
from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

import httpx

class ImmichTools:
    def __init__(self):

        self.immich_api_key = os.getenv("IMMICH_API_KEY")
        self.immich_base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283/api")
        self.http_client = httpx.AsyncClient(
            base_url=self.immich_base_url,
            headers={"x-api-key": self.immich_api_key},
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
