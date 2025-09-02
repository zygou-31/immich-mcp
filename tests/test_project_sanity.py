from mcp.server.fastmcp import FastMCP

from immich_mcp.server import mcp


def test_server_instance_exists():
    """Tests that the FastMCP server instance is created."""
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "ImmichMCP"
