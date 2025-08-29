from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from .immich_api import ImmichAPI


class AppContext(TypedDict):
    """Application context holding shared resources."""

    immich_client: ImmichAPI


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage the application's lifespan, creating and cleaning up resources."""
    # The ImmichAPI client will fetch credentials from environment variables.
    # It will raise a ValueError if they are not set.
    async with ImmichAPI() as immich_client:
        yield AppContext(immich_client=immich_client)


# Pass the lifespan manager to the server instance
mcp = FastMCP(name="ImmichMCP", lifespan=app_lifespan)


@mcp.tool()
async def ping(ctx: Context[ServerSession, AppContext]) -> str:
    """
    Pings the real Immich server to check for a valid connection.
    Returns 'pong' if successful, otherwise returns an error message.
    """
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    if await immich_client.ping_server():
        return "pong"
    return "error: could not connect to Immich server"
