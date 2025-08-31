#!/bin/bash
run_and_interact() {
  IMMICH_API_URL="$1" IMMICH_API_KEY="$2" nohup python tmp_mcp_run3.py >/tmp/mcp.log 2>&1 &
  PID=$!
  echo "started pid $PID"
  for i in {1..30}; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8003/ || true)
    if [ "$CODE" != "000" ]; then
      echo "server HTTP code: $CODE"
      break
    fi
    sleep 0.2
  done
  sleep 0.2
  echo "--- initialize ---"
  INIT='{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","clientInfo":{"name":"test","version":"0.1"},"capabilities":{}},"id":"init"}'
  RESP=$(curl -i -s -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -d "$INIT")
  echo "$RESP" | sed -n '1,120p'
  SID=$(echo "$RESP" | awk -F': ' '/mcp-session-id/{print $2}' | tr -d '\r' | head -1)
  echo "session id: $SID"
  echo "--- init notify ---"
  NOTIFY='{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'
  curl -s -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$NOTIFY" >/dev/null
  echo "--- tools/list (first chunk) ---"
  LIST='{"jsonrpc":"2.0","method":"tools/list","params":{},"id":"list1"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$LIST" | sed -n '1,5p'
  echo "--- tools/call ping (first chunk) ---"
  CALL='{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ping","arguments":{}},"id":"ping1"}'
  curl -s -N -X POST http://127.0.0.1:8003/mcp -H 'Accept: application/json, text/event-stream' -H 'Content-Type: application/json' -H "mcp-session-id: $SID" -d "$CALL" | sed -n '1,5p'
  kill $PID || true
  sleep 0.2
}

echo '=== Real IMMICH env (may fail if Immich not running) ==='
run_and_interact http://localhost:2283/api Q4jdjegBu4OJC3rrZESsbNRGxHX70aEQUo7kSdUVs

echo '\n=== Dummy IMMICH env (simulate down) ==='
run_and_interact http://127.0.0.1:59999 dummy
