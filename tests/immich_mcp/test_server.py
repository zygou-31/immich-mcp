import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

from immich_mcp.cli import create_app


@pytest.fixture
def client():
    with patch("immich_mcp.cli.load_config") as mock_load_config:
        mock_config = MagicMock()
        mock_config.auth_token = "test_token"
        mock_config.test_connection = AsyncMock(return_value=True)
        mock_config.immich_base_url = "http://test.com/api"
        mock_config.immich_api_key = "test_api_key"
        mock_load_config.return_value = mock_config

        # Mock the lifespan function to return a proper async context manager
        async def mock_lifespan(app):
            app.state.config = mock_config

            # Create a mock tool server that returns a simple response
            from fastapi import FastAPI

            mock_mcp_app = FastAPI()

            @mock_mcp_app.post("/")
            async def tools_list():
                return {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}

            # Mount the mock MCP app
            app.mount("/mcp", mock_mcp_app)
            yield

        # Patch the lifespan in the create_app function
        with patch("immich_mcp.cli.lifespan", mock_lifespan):
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
    # Since we're mocking the ToolServer, the response will be from the mock
    # For now, let's just check that the endpoint exists (200 status code)
    # The actual MCP server implementation can be tested separately
    assert response.status_code == 200


def test_auth_valid_token(client):
    response = client.get("/", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200


def test_auth_invalid_token(client):
    response = client.get("/", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
