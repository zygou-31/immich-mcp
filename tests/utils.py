import time

from httpx import AsyncClient


async def initialize_session(client: AsyncClient) -> str:
    """Perform the MCP initialize handshake and return a session ID."""
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "clientInfo": {"name": "immich-mcp-test-client", "version": "0.1.0"},
            "capabilities": {},
        },
        "id": "init1",
    }
    headers = {"Accept": "application/json, text/event-stream"}
    response = await client.post("/mcp", json=init_request, headers=headers)
    response.raise_for_status()
    time.sleep(0.1)
    session_id = response.headers["mcp-session-id"]
    # Complete the initialization handshake with the correct notification
    init_notify = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    notify_headers = {
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id,
    }
    notify_resp = await client.post("/mcp", json=init_notify, headers=notify_headers)
    notify_resp.raise_for_status()
    return session_id
