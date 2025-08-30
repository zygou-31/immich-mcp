MCP Initialization Handshake

When a client connects to the MCP `streamable-http` endpoint, it must perform
an initialization sequence before issuing requests like `tools/call`.

Required steps (tests rely on this):
- POST a JSON-RPC `initialize` request to `/mcp` and read the `mcp-session-id`
  response header.
- POST a JSON-RPC notification with method `notifications/initialized` and
  include the `mcp-session-id` header to complete the handshake.

Example (HTTP client):
- `POST /mcp` body: {"jsonrpc":"2.0","method":"initialize","params":{...},"id":"init1"}
- Read header `mcp-session-id` from response.
- `POST /mcp` body: {"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
  with header `mcp-session-id: <value>`

If the `notifications/initialized` notification is not sent, the server may
reject subsequent requests with `Invalid request parameters` while the
initialization is considered incomplete.

