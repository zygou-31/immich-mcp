import json
import pytest
from pytest_mock import MockerFixture

from immich_mcp_server import server
from immich_mcp_server.immich_api import ImmichAPI


@pytest.mark.asyncio
async def test_get_user_resource(mocker: MockerFixture):
    """Tests that the user resource correctly returns a mock user."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_my_user.return_value = {
        "id": "test-user-id",
        "email": "test@example.com",
        "name": "Test User",
    }

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    user = await server.get_user()

    assert user is not None
    assert user["id"] == "test-user-id"
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_users_list_resource(mocker: MockerFixture):
    """Tests that the users resource correctly returns a mock list of users."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_users_list.return_value = [
        {"id": "user1", "email": "user1@example.com", "name": "User One"},
        {"id": "user2", "email": "user2@example.com", "name": "User Two"},
    ]

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    users_list = await server.get_users_list()

    assert len(users_list) == 2
    assert users_list[0]["name"] == "User One"
    assert users_list[1]["email"] == "user2@example.com"


@pytest.mark.asyncio
async def test_get_partners_resource(mocker: MockerFixture):
    """Tests that the partners resource correctly returns a mock list of partners."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_partners.return_value = [
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

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    partners_list = await server.get_partners()

    assert len(partners_list) == 2
    assert partners_list[0]["name"] == "Partner One"
    assert partners_list[0]["inTimeline"] is True
    assert partners_list[1]["email"] == "partner2@example.com"
    assert partners_list[1]["inTimeline"] is False


@pytest.mark.asyncio
async def test_get_asset_resource(mocker: MockerFixture):
    """Tests that the asset resource correctly returns a mock asset."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_asset.return_value = {
        "id": "asset1",
        "originalFileName": "test.jpg",
        "type": "IMAGE",
    }

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    asset = await server.get_asset("asset1")

    assert asset is not None
    assert asset["id"] == "asset1"
    assert asset["originalFileName"] == "test.jpg"
    assert asset["type"] == "IMAGE"


@pytest.mark.asyncio
async def test_get_my_api_key_resource(mocker: MockerFixture):
    """Tests that the my_api_key resource correctly returns a mock api key."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_my_api_key.return_value = {
        "id": "api-key-1",
        "name": "My API Key",
    }

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    api_key = await server.get_my_api_key()

    assert api_key is not None
    assert api_key["id"] == "api-key-1"
    assert api_key["name"] == "My API Key"


@pytest.mark.asyncio
async def test_get_api_key_list_resource(mocker: MockerFixture):
    """Tests that the api_keys resource correctly returns a mock list of api keys."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_api_key_list.return_value = [
        {"id": "api-key-1", "name": "API Key 1"},
        {"id": "api-key-2", "name": "API Key 2"},
    ]

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    api_key_list = await server.get_api_key_list()

    assert len(api_key_list) == 2
    assert api_key_list[0]["name"] == "API Key 1"
    assert api_key_list[1]["id"] == "api-key-2"


@pytest.mark.asyncio
async def test_get_api_key_resource(mocker: MockerFixture):
    """Tests that the api_key resource correctly returns a mock api key."""
    mock_immich_client = mocker.AsyncMock(spec=ImmichAPI)
    mock_immich_client.get_api_key.return_value = {
        "id": "api-key-1",
        "name": "API Key 1",
    }

    mock_context = mocker.MagicMock()
    mock_context.request_context.lifespan_context = {"immich_client": mock_immich_client}
    mocker.patch.object(server.mcp, "get_context", return_value=mock_context)

    api_key = await server.get_api_key("api-key-1")

    assert api_key is not None
    assert api_key["id"] == "api-key-1"
    assert api_key["name"] == "API Key 1"
