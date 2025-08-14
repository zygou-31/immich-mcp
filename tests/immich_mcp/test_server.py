import pytest
from unittest.mock import patch, MagicMock
from immich_mcp.server import create_mcp_server


@patch("immich_mcp.server.load_config")
class TestCreateMCP:
    """Test cases for the create_mcp_server function."""

    @patch("asyncio.run")
    def test_create_mcp_server_success(self, mock_asyncio_run, mock_load_config):
        """Test successful creation of MCP server."""
        # Mock configuration
        mock_config = MagicMock()
        mock_load_config.return_value = mock_config

        # Mock asyncio.run to return True (successful connection)
        mock_asyncio_run.return_value = True

        # Create the server
        server = create_mcp_server()

        # Verify the server was created
        assert server is not None
        assert server.name == "Immich MCP Server"

        # Verify config was loaded
        mock_load_config.assert_called_once()

        # Verify connection test was called
        mock_asyncio_run.assert_called_once()

    @patch("asyncio.run")
    def test_create_mcp_server_connection_failure(
        self, mock_asyncio_run, mock_load_config
    ):
        """Test MCP server creation when connection fails."""
        # Mock configuration
        mock_config = MagicMock()
        mock_load_config.return_value = mock_config

        # Mock asyncio.run to return False (failed connection)
        mock_asyncio_run.return_value = False

        # Create the server (should still work even with connection failure)
        server = create_mcp_server()

        # Verify the server was created
        assert server is not None
        assert server.name == "Immich MCP Server"

        # Verify config was loaded
        mock_load_config.assert_called_once()

        # Verify connection test was called
        mock_asyncio_run.assert_called_once()

    def test_create_mcp_server_config_error(self, mock_load_config):
        """Test MCP server creation when config loading fails."""
        # Mock configuration loading to raise an exception
        mock_load_config.side_effect = Exception("Config error")

        # Attempt to create the server (should raise the exception)
        with pytest.raises(Exception) as exc_info:
            create_mcp_server()

        # Verify the exception message
        assert "Config error" in str(exc_info.value)
