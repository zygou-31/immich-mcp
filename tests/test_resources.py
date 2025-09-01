import json
import os
import pytest
import pytest_asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest_asyncio.fixture
async def client_session():
    """Provides a client session connected to the server."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.immich_mcp_server.server"],
        env={
            **os.environ,
            "TESTING": "1",
            "PYTHONPATH": "src",
        },
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
async def test_get_user_resource(client_session: ClientSession):
    """Tests that the user resource correctly returns a mock user."""
    result = await client_session.read_resource("user://me")
    user = json.loads(result.contents[0].text)

    assert user is not None
    assert user["id"] == "test-user-id"
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_users_list_resource(client_session: ClientSession):
    """Tests that the users resource correctly returns a mock list of users."""
    result = await client_session.read_resource("users://list")
    users_list = json.loads(result.contents[0].text)

    assert len(users_list) == 2
    assert users_list[0]["name"] == "User One"
    assert users_list[1]["email"] == "user2@example.com"


@pytest.mark.asyncio
async def test_get_partners_resource(client_session: ClientSession):
    """Tests that the partners resource correctly returns a mock list of partners."""
    result = await client_session.read_resource("partners://list")
    partners_list = json.loads(result.contents[0].text)

    assert len(partners_list) == 2
    assert partners_list[0]["name"] == "Partner One"
    assert partners_list[0]["inTimeline"] is True
    assert partners_list[1]["email"] == "partner2@example.com"
    assert partners_list[1]["inTimeline"] is False


@pytest.mark.asyncio
async def test_get_asset_resource(client_session: ClientSession):
    """Tests that the asset resource correctly returns a mock asset."""
    result = await client_session.read_resource("asset://asset1")
    asset = json.loads(result.contents[0].text)

    assert asset is not None
    assert asset["id"] == "asset1"
    assert asset["originalFileName"] == "test.jpg"
    assert asset["type"] == "IMAGE"


@pytest.mark.asyncio
async def test_get_my_api_key_resource(client_session: ClientSession):
    """Tests that the my_api_key resource correctly returns a mock api key."""
    result = await client_session.read_resource("apikey://me")
    api_key = json.loads(result.contents[0].text)

    assert api_key is not None
    assert api_key["id"] == "api-key-1"
    assert api_key["name"] == "My API Key"


@pytest.mark.asyncio
async def test_get_api_key_list_resource(client_session: ClientSession):
    """Tests that the api_keys resource correctly returns a mock list of api keys."""
    result = await client_session.read_resource("apikeys://list")
    api_key_list = json.loads(result.contents[0].text)

    assert len(api_key_list) == 2
    assert api_key_list[0]["name"] == "API Key 1"
    assert api_key_list[1]["id"] == "api-key-2"


@pytest.mark.asyncio
async def test_get_api_key_resource(client_session: ClientSession):
    """Tests that the api_key resource correctly returns a mock api key."""
    result = await client_session.read_resource("apikey://api-key-1")
    api_key = json.loads(result.contents[0].text)

    assert api_key is not None
    assert api_key["id"] == "api-key-1"
    assert api_key["name"] == "API Key 1"
