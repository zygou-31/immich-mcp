import json
import os
import threading
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
import uvicorn
from httpx import AsyncClient

from immich_mcp.immich_api import ImmichAPI
from immich_mcp.server import mcp
from tests.utils import initialize_session


class UvicornTestServer(uvicorn.Server):
    """Uvicorn test server that runs in a thread."""

    def __init__(self, app, host="127.0.0.1", port=8000):
        self._startup_done = threading.Event()
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        super().__init__(config)

    def run_in_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self._startup_done.wait(timeout=5)
        if not self._startup_done.is_set():
            raise RuntimeError("Server did not start in time.")

    def stop(self):
        self.should_exit = True
        self.thread.join(timeout=5)
        if self.thread.is_alive():
            raise RuntimeError("Server did not stop in time.")

    async def startup(self, sockets=None):
        await super().startup(sockets=sockets)
        self._startup_done.set()


@pytest_asyncio.fixture(scope="module")
async def server():
    """Fixture to run the MCP server in a background thread."""
    app = mcp.streamable_http_app()
    server = UvicornTestServer(app)
    server.run_in_thread()
    yield f"http://{server.config.host}:{server.config.port}"
    server.stop()


# `initialize_session` moved to `tests/utils.py` and imported above.


@pytest.mark.asyncio
@patch.dict(os.environ, {"IMMICH_BASE_URL": "http://test.com", "IMMICH_API_KEY": "test-key"})
@patch(
    "immich_mcp.immich_api.ImmichAPI.ping_server",
    new_callable=AsyncMock,
    return_value=True,
)
async def test_ping_tool_success(mock_ping_server, server: str):
    """Tests the ping tool against a running server."""
    async with AsyncClient(base_url=server) as client:
        session_id = await initialize_session(client)

        tool_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "ping", "arguments": {}},
            "id": "1",
        }
        headers = {
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": session_id,
        }

        async with client.stream("POST", "/mcp", json=tool_request, headers=headers) as response:
            response.raise_for_status()
            sse_event = await response.aiter_bytes().__anext__()
            data_part = sse_event.split(b"data: ")[1].strip()
            tool_result = json.loads(data_part)

            assert tool_result["id"] == "1"
            assert "result" in tool_result
            assert tool_result["result"]["content"][0]["text"] == "pong"


@pytest.mark.asyncio
@patch.dict(os.environ, {"IMMICH_BASE_URL": "http://test.com", "IMMICH_API_KEY": "test-key"})
@patch(
    "immich_mcp.immich_api.ImmichAPI.ping_server",
    new_callable=AsyncMock,
    return_value=False,
)
async def test_ping_tool_failure(mock_ping_server, server: str):
    """Tests the ping tool with a mocked failed connection."""
    async with AsyncClient(base_url=server) as client:
        session_id = await initialize_session(client)

        tool_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "ping", "arguments": {}},
            "id": "2",
        }
        headers = {
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": session_id,
        }
        async with client.stream("POST", "/mcp", json=tool_request, headers=headers) as response:
            response.raise_for_status()
            sse_event = await response.aiter_bytes().__anext__()
            data_part = sse_event.split(b"data: ")[1].strip()
            tool_result = json.loads(data_part)

            assert tool_result["id"] == "2"
            assert "result" in tool_result
            assert "error: could not connect" in tool_result["result"]["content"][0]["text"]


def test_immich_api_raises_on_missing_env_vars():
    """
    Tests that the ImmichAPI class raises a ValueError if the required
    environment variables are not set.
    """
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Immich base URL must be provided"):
            ImmichAPI()
