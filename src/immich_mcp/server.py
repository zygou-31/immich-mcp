import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import List, TypedDict

from mcp.server.fastmcp import FastMCP

if os.environ.get("TESTING"):
    from tests.fake_immich_api import ImmichAPI
else:
    from immich_mcp.immich_api import ImmichAPI


class User(TypedDict):
    """Represents a user in Immich."""

    id: str
    email: str
    name: str


UsersList = List[User]


class Partner(User):
    """Represents a partner in Immich."""

    inTimeline: bool


PartnersList = List[Partner]


class Asset(TypedDict):
    """Represents an asset in Immich."""

    id: str
    originalFileName: str
    type: str


class ApiKey(TypedDict):
    """Represents an API key in Immich."""

    id: str
    name: str
    createdAt: str
    updatedAt: str
    permissions: List[str]


ApiKeyList = List[ApiKey]


class AppContext(TypedDict):
    """Application context holding shared resources."""

    immich_client: ImmichAPI


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage the application's lifespan, creating and cleaning up resources."""
    print("Initializing app lifespan")
    async with ImmichAPI() as immich_client:
        print("ImmichAPI client created")
        yield AppContext(immich_client=immich_client)
    print("App lifespan finished")


mcp = FastMCP(name="ImmichMCP", lifespan=app_lifespan)


@mcp.tool()
async def ping() -> str:
    """
    Pings the real Immich server to check for a valid connection.
    Returns 'pong' if successful, otherwise returns an error message.
    """
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    if await immich_client.ping_server():
        return "pong"
    return "error: could not connect to Immich server"


@mcp.resource("user://me")
async def get_user() -> User | None:
    """Returns the current user's details."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    user_data = await immich_client.get_my_user()
    if not user_data:
        raise ValueError("Failed to fetch user from Immich API")
    return User(id=user_data["id"], email=user_data["email"], name=user_data["name"])


@mcp.resource("users://list")
async def get_users_list() -> UsersList:
    """Returns a list of all users."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    users_data = await immich_client.get_users_list()
    return [User(id=user["id"], email=user["email"], name=user["name"]) for user in users_data]


@mcp.resource("partners://list")
async def get_partners() -> PartnersList:
    """Returns a list of all partners."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    partners_data = await immich_client.get_partners()
    return [
        Partner(
            id=partner["id"],
            email=partner["email"],
            name=partner["name"],
            inTimeline=partner["inTimeline"],
        )
        for partner in partners_data
    ]


@mcp.resource("asset://{asset_id}")
async def get_asset(asset_id: str) -> Asset | None:
    """Returns an asset by its ID."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    asset_data = await immich_client.get_asset(asset_id)
    if not asset_data:
        return None
    return Asset(
        id=asset_data["id"],
        originalFileName=asset_data["originalFileName"],
        type=asset_data["type"],
    )


@mcp.resource("apikey://me")
async def get_my_api_key() -> ApiKey | None:
    """Returns the current API key's details."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    api_key_data = await immich_client.get_my_api_key()
    if not api_key_data:
        return None
    return ApiKey(
        id=api_key_data["id"],
        name=api_key_data["name"],
        createdAt=api_key_data["createdAt"],
        updatedAt=api_key_data["updatedAt"],
        permissions=api_key_data["permissions"],
    )


@mcp.resource("apikeys://list")
async def get_api_key_list() -> ApiKeyList:
    """Returns a list of all API keys."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    api_keys_data = await immich_client.get_api_key_list()
    return [
        ApiKey(
            id=key["id"],
            name=key["name"],
            createdAt=key["createdAt"],
            updatedAt=key["updatedAt"],
            permissions=key["permissions"],
        )
        for key in api_keys_data
    ]


@mcp.resource("apikey://{api_key_id}")
async def get_api_key(api_key_id: str) -> ApiKey | None:
    """Returns an API key by its ID."""
    ctx = mcp.get_context()
    immich_client = ctx.request_context.lifespan_context["immich_client"]
    api_key_data = await immich_client.get_api_key(api_key_id)
    if not api_key_data:
        return None
    return ApiKey(
        id=api_key_data["id"],
        name=api_key_data["name"],
        createdAt=api_key_data["createdAt"],
        updatedAt=api_key_data["updatedAt"],
        permissions=api_key_data["permissions"],
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
