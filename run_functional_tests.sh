#!/bin/bash

# Function to run the server and interact with it
run_and_interact() {
  echo "--- Starting MCP server ---"
  # Use uv run to run the server
  uv run uvicorn src.immich_mcp.main:app --port 8003 >/tmp/mcp.log 2>&1 &
  PID=$!
  echo "Server started with PID $PID"

  # Wait for the server to start
  for i in {1..30}; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8003/mcp || true)
    if [ "$CODE" == "405" ]; then
      echo "Server is up, HTTP code: $CODE"
      break
    fi
    sleep 0.2
  done
  sleep 0.2

  echo "--- Initializing session ---"
  INIT='{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","clientInfo":{"name":"test","version":"0.1"},"capabilities":{}},"id":"init"}'
  RESP=$(curl -i -s -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -d "$INIT")
  SID=$(echo "$RESP" | awk -F': ' '/mcp-session-id/{print $2}' | tr -d '\r' | head -1)
  echo "Session ID: $SID"

  echo "--- Sending initialized notification ---"
  NOTIFY='{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'
  curl -s -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$NOTIFY" >/dev/null

  echo "--- Listing all resources ---"
  LIST='{"jsonrpc":"2.0","method":"resources/list","params":{},"id":"list1"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$LIST"

  echo -e "\n--- Reading user://me resource ---"
  READ_USER='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"user://me"},"id":"read_user"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_USER"

  echo -e "\n--- Reading users://list resource ---"
  READ_USERS='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"users://list"},"id":"read_users"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_USERS"

  echo -e "\n--- Reading partners://list resource ---"
  READ_PARTNERS='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"partners://list"},"id":"read_partners"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_PARTNERS"

  echo -e "\n--- Reading apikey://me resource ---"
  READ_MY_API_KEY='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"apikey://me"},"id":"read_my_api_key"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_MY_API_KEY"

  echo -e "\n--- Reading apikeys://list resource ---"
  READ_API_KEY_LIST='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"apikeys://list"},"id":"read_api_key_list"}'
  API_KEY_LIST_RESP=$(curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_API_KEY_LIST")
  echo "$API_KEY_LIST_RESP"

  # Extract the first API key ID from the response
  API_KEY_ID=$(echo "$API_KEY_LIST_RESP" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo "Extracted API Key ID: $API_KEY_ID"

  if [ -n "$API_KEY_ID" ]; then
    echo -e "\n--- Reading apikey://{id} resource with ID: $API_KEY_ID ---"
    READ_API_KEY='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"apikey://'$API_KEY_ID'"},"id":"read_api_key"}'
    curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_API_KEY"
  else
    echo -e "\n--- Skipping apikey://{id} read, no API key ID found ---"
  fi

  echo -e "\n--- Reading asset://{id} resource ---"
  READ_ASSET='{"jsonrpc":"2.0","method":"resources/read","params":{"uri":"asset://58cb6484-a03a-4d29-8cca-249d5bfc1611"},"id":"read_asset"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$READ_ASSET"

  echo "--- Shutting down server ---"
  kill $PID || true
  sleep 0.2
}

# Check if IMMICH_BASE_URL and IMMICH_API_KEY are set
if [ -z "$IMMICH_BASE_URL" ] || [ -z "$IMMICH_API_KEY" ]; then
  echo "Error: IMMICH_BASE_URL and IMMICH_API_KEY environment variables must be set."
  exit 1
fi

run_and_interact
