import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

from main import create_app

@pytest.fixture
def client():
    with patch("main.load_config") as mock_load_config:
        mock_config = MagicMock()
        mock_config.auth_token = "test_token"
        mock_config.test_connection = AsyncMock(return_value=True)
        mock_load_config.return_value = mock_config

        app = create_app()
        with TestClient(app) as client:
            yield client

def test_tools_list(client):
    response = client.post(
        "/mcp",
        headers={"Authorization": "Bearer test_token"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["jsonrpc"] == "2.0"
    assert response_json["id"] == 1
    assert "result" in response_json

    result = response_json["result"]
    assert isinstance(result, dict)
    assert "tools" in result
    tools = result["tools"]
    assert isinstance(tools, list)
    assert len(tools) == 6
    expected_tool_names = [
        "ping_server",
        "get_all_albums",
        "get_asset_info",
        "search_photos",
        "upload_photo",
        "create_album",
    ]
    actual_tool_names = [tool["name"] for tool in tools]
    assert sorted(actual_tool_names) == sorted(expected_tool_names)

def test_auth_valid_token(client):
    response = client.get(
        "/", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200

def test_auth_invalid_token(client):
    response = client.get(
        "/", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
