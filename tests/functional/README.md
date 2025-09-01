Purpose
-------
This document describes how to manually test the `ping` tool against a running Immich instance and suggests functional tests that exercise real-world behavior. These tests are intentionally kept out of unit test suites because they require a live Immich server.

Prerequisites
-------------
- A running Immich instance reachable via `IMMICH_API_URL`.
- A valid `IMMICH_API_KEY` for that instance.
- Python virtual environment with project dependencies installed.

Quick test (scripted)
---------------------
There is a helper script `run_test_ping.sh` in the repository that automates the following flow. To run it:

1. Export environment variables or pass them to the script invocation:

   - `IMMICH_API_URL` — The full URL to your Immich API, including the `/api` path (e.g., `http://localhost:2283/api`).
   - `IMMICH_API_KEY` — your Immich API key

2. Run the script:

   ```bash
   bash run_test_ping.sh
   ```

This script starts the MCP server, initializes a session, lists available tools and calls the `ping` tool. It repeats the flow with a dummy Immich URL to simulate an unreachable Immich server.

Manual steps (concise)
----------------------
- Start the MCP server (example):
  - `uv run mcp dev src/immich_mcp_server/server.py` or use the provided `tmp_mcp_run3.py`/`uvicorn` invocation.
- Initialize an MCP session by POSTing an `initialize` request to `/mcp` and capture the `mcp-session-id` header.
- Send `notifications/initialized` with the `mcp-session-id` header.
- Call `tools/list` to confirm the `ping` tool is present.
- Call `tools/call` with `name: "ping"` and expect the textual content `pong` when the Immich server is reachable.
- Repeat the call flow with `IMMICH_API_URL` pointing to a non-routable/dummy address and expect a friendly error message (for example: `error: could not connect to Immich server`).

Functional test ideas (for manual or gated CI)
---------------------------------------------
- Successful ping: MCP `tools/call` returns `pong` when Immich is reachable.
- Unreachable Immich: MCP returns a friendly error message instead of raising an exception.
- Non-JSON or malformed response: MCP should handle JSON decode errors and return a friendly error.
- Timeout behavior: if the client adds a short request timeout, verify that unreachable hosts fail quickly and return the friendly error.

Notes
-----
- Keep these tests out of the unit test suite since they require a real Immich instance.
- Consider a separate integration test workflow or an opt-in CI job that runs these functional tests in an environment with a provisioned Immich instance.

