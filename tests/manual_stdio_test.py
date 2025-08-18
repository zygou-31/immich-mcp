import asyncio
import os
import sys

import pytest

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


async def run_test():
    # Ensure env vars exist for tests
    env = os.environ.copy()
    env["IMMICH_BASE_URL"] = env.get("IMMICH_BASE_URL", "https://example.com/api")
    env["IMMICH_API_KEY"] = env.get("IMMICH_API_KEY", "dummykey1234567890")
    env["IMMICH_AUTH_TOKEN"] = env.get("IMMICH_AUTH_TOKEN", "dummyauthtoken123")
    env["DISABLE_CONSOLE_OUTPUT"] = "true"

    # Pass a minimal env to the spawned process with only IMMICH_* variables
    spawned_env = {
        "IMMICH_BASE_URL": env["IMMICH_BASE_URL"],
        "IMMICH_API_KEY": env["IMMICH_API_KEY"],
        "IMMICH_AUTH_TOKEN": env["IMMICH_AUTH_TOKEN"],
        "DISABLE_CONSOLE_OUTPUT": "true",
        # Ensure the spawned main process does not start HTTP services during this stdio test
        "DISABLE_STREAMABLE_HTTP": "true",
        "DISABLE_UVICORN": "true",
        # Indicate we're running in stdio mode
        "MCP_MODE": "stdio",
    }

    # Use mock stdio server for fast tests if requested
    use_mock = os.environ.get("USE_MOCK_STDIO", "true").lower() == "true"
    if use_mock:
        from tests._mock_stdio import mock_stdio_server

        async with mock_stdio_server() as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                tools = await session.list_tools()
                return list(tools)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "main", "--mode", "stdio"],
        env=spawned_env,
    )

    async with stdio_client(server_params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = await session.list_tools()
            tools_list = list(tools)
            # Return the list for assertions in the pytest wrapper
            return tools_list


@pytest.mark.asyncio
async def test_manual_stdio_run():
    """Manual stdio test run under pytest. This may be skipped if the 'mcp' package is missing."""
    try:
        tools = await run_test()
    except ModuleNotFoundError as e:
        pytest.skip(f"Skipping manual stdio test due to missing dependency: {e}")
    except Exception as e:
        pytest.fail(f"Manual stdio test failed during run: {e}")

    assert isinstance(tools, (list, tuple)), "Expected tools to be a list or tuple"


if __name__ == "__main__":
    asyncio.run(run_test())
