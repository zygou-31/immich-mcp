import anyio
import sys
from contextlib import asynccontextmanager
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage


@asynccontextmanager
async def mock_stdio_server():
    """Provide read_stream, write_stream compatible with mcp client stdio.

    The mock responds to initialize and list_tools calls.
    """
    # create memory object streams matching stdio_server implementation
    read_send, read_receive = anyio.create_memory_object_stream(0)
    write_send, write_receive = anyio.create_memory_object_stream(0)

    async def server_loop():
        async with read_send, write_send:
            async for session_msg in read_receive:
                try:
                    # session_msg is SessionMessage containing a JSONRPCMessage
                    msg = session_msg.message
                    md = msg.model_dump()
                    # access method and id from dict form to avoid attribute case issues
                    method = md.get("method")
                    req_id = md.get("id")
                    # limited debug output
                    print(
                        f"[mock_stdio] received method={method} id={req_id} msg={md}",
                        file=sys.stderr,
                    )

                    # Normalize method name
                    method_norm = (method or "").lower()

                    # Prepare response payload dict
                    if method_norm == "initialize":
                        result = {
                            "protocolVersion": md.get("params", {}).get(
                                "protocolVersion", "2025-06-18"
                            ),
                            "capabilities": {},
                            "serverInfo": {"name": "immich-mock", "version": "0.0.0"},
                        }
                    elif method_norm in (
                        "listtoolsrequest",
                        "listtools",
                        "list_tools",
                        "tools/list",
                    ):
                        # minimal tools list — wrap in a dict so JSONRPC response 'result' is an object
                        result = {
                            "tools": [
                                {
                                    "name": "ping",
                                    "title": "Ping",
                                    "description": "Ping tool",
                                    "inputSchema": {},
                                    "outputSchema": {},
                                }
                            ]
                        }
                    else:
                        # No response for notifications or unknown methods without id
                        result = None

                    if req_id is not None:
                        # Build JSON-RPC response message using same model class
                        response_obj = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": result,
                        }
                        # validate and create SessionMessage
                        try:
                            resp = SessionMessage(
                                JSONRPCMessage.model_validate(response_obj)
                            )
                        except Exception as e:
                            print(
                                f"[mock_stdio] response validation error: {e}",
                                file=sys.stderr,
                            )
                            raise
                        await write_send.send(resp)
                        print(
                            f"[mock_stdio] sent response id={req_id}", file=sys.stderr
                        )
                except Exception as e:
                    print(f"[mock_stdio] error: {e}", file=sys.stderr)
                    continue

    async with anyio.create_task_group() as tg:
        tg.start_soon(server_loop)
        # yield the client's read and write streams: client reads from write_receive, writes to read_send
        try:
            yield write_receive, read_send
        finally:
            # task group will exit when context closes; cancel scope not available on TaskGroup
            pass
