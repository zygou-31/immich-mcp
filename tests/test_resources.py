from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture

from immich_mcp.server import (
    get_api_key,
    get_api_key_list,
    get_asset,
    get_my_api_key,
    get_partners,
    get_user,
    get_users_list,
)


@pytest_asyncio.fixture
def mock_mcp_context(mocker: MockerFixture):
    """Provides a mock MCP context with a mocked ImmichAPI client."""
    mock_context = mocker.patch("immich_mcp.server.mcp.get_context")
    mock_api_client = AsyncMock()
    mock_context.return_value.request_context.lifespan_context = {"immich_client": mock_api_client}
    mock_context.return_value.api_key = "my-fake-api-key"
    return mock_context


@pytest.mark.asyncio
async def test_get_user_resource(mock_mcp_context):
    """Tests that the user resource correctly returns a mock user."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_my_user.return_value = {
        "id": "test-user-id",
        "email": "test@example.com",
        "name": "Test User",
    }

    user = await get_user()

    assert user is not None
    assert user["id"] == "test-user-id"
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"
    mock_api_client.get_my_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_users_list_resource(mock_mcp_context):
    """Tests that the users resource correctly returns a mock list of users."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_users_list.return_value = [
        {"id": "user1", "email": "user1@example.com", "name": "User One"},
        {"id": "user2", "email": "user2@example.com", "name": "User Two"},
    ]

    users_list = await get_users_list()

    assert len(users_list) == 2
    assert users_list[0]["name"] == "User One"
    assert users_list[1]["email"] == "user2@example.com"
    mock_api_client.get_users_list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_partners_resource(mock_mcp_context):
    """Tests that the partners resource correctly returns a mock list of partners."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_partners.return_value = [
        {
            "id": "partner1",
            "email": "partner1@example.com",
            "name": "Partner One",
            "inTimeline": True,
        },
        {
            "id": "partner2",
            "email": "partner2@example.com",
            "name": "Partner Two",
            "inTimeline": False,
        },
    ]
    partners_list = await get_partners()

    assert len(partners_list) == 2
    assert partners_list[0]["name"] == "Partner One"
    assert partners_list[0]["inTimeline"] is True
    assert partners_list[1]["email"] == "partner2@example.com"
    assert partners_list[1]["inTimeline"] is False
    mock_api_client.get_partners.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_asset_resource(mock_mcp_context):
    """Tests that the asset resource correctly returns a mock asset."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_asset.return_value = {
        "id": "asset1",
        "originalFileName": "test.jpg",
        "type": "IMAGE",
    }
    asset = await get_asset(asset_id="asset1")

    assert asset is not None
    assert asset["id"] == "asset1"
    assert asset["originalFileName"] == "test.jpg"
    assert asset["type"] == "IMAGE"
    mock_api_client.get_asset.assert_awaited_once_with("asset1")


@pytest.mark.asyncio
async def test_get_my_api_key_resource(mock_mcp_context):
    """Tests that the my_api_key resource correctly returns the current api key."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_my_api_key.return_value = {
        "id": "api-key-me",
        "name": "My API Key",
        "createdAt": "2025-09-02T00:00:00Z",
        "updatedAt": "2025-09-02T00:00:00Z",
        "permissions": ["all"],
    }
    api_key = await get_my_api_key()

    assert api_key is not None
    assert api_key["id"] == "api-key-me"
    mock_api_client.get_my_api_key.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_api_key_list_resource(mock_mcp_context):
    """Tests that the api_keys resource correctly returns a mock list of api keys."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_api_key_list.return_value = [
        {
            "id": "api-key-1",
            "name": "API Key 1",
            "createdAt": "2025-09-02T00:00:00Z",
            "updatedAt": "2025-09-02T00:00:00Z",
            "permissions": ["all"],
        },
        {
            "id": "api-key-2",
            "name": "API Key 2",
            "createdAt": "2025-09-02T00:00:00Z",
            "updatedAt": "2025-09-02T00:00:00Z",
            "permissions": ["all"],
        },
    ]
    api_key_list = await get_api_key_list()

    assert len(api_key_list) == 2
    assert api_key_list[0]["name"] == "API Key 1"
    assert api_key_list[1]["id"] == "api-key-2"
    mock_api_client.get_api_key_list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_api_key_resource(mock_mcp_context):
    """Tests that the api_key resource correctly returns a mock api key."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_api_key.return_value = {
        "id": "api-key-1",
        "name": "API Key 1",
        "createdAt": "2025-09-02T00:00:00Z",
        "updatedAt": "2025-09-02T00:00:00Z",
        "permissions": ["all"],
    }
    api_key = await get_api_key(api_key_id="api-key-1")

    assert api_key is not None
    assert api_key["id"] == "api-key-1"
    assert api_key["name"] == "API Key 1"
    mock_api_client.get_api_key.assert_awaited_once_with("api-key-1")


@pytest.mark.asyncio
async def test_get_user_resource_error(mock_mcp_context):
    """Tests that the user resource correctly raises an error."""
    mock_api_client = mock_mcp_context.return_value.request_context.lifespan_context["immich_client"]
    mock_api_client.get_my_user.return_value = {}  # Simulate empty response

    with pytest.raises(ValueError) as excinfo:
        await get_user()

    assert "Failed to fetch user from Immich API" in str(excinfo.value)
    mock_api_client.get_my_user.assert_awaited_once()
