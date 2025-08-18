"""
Stdio bridge for Immich MCP server.

This module provides a stdio-based MCP server implementation that can communicate
over stdin/stdout, enabling integration with Claude Desktop and other MCP clients.
"""

import asyncio
import logging
import sys
import os
from typing import Optional

# mcp server stdio classes
from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool

from immich_mcp.client import ImmichClient
from immich_mcp.config import ImmichConfig, load_config
from immich_mcp.tools import ImmichTools

# Set up logging
# If DISABLE_CONSOLE_OUTPUT is true, we must avoid printing anything to stdout
# because stdout is the JSON-RPC channel. All logs will go to stderr.
DISABLE_STDOUT = (
    "DISABLE_CONSOLE_OUTPUT" in os.environ
    and os.environ.get("DISABLE_CONSOLE_OUTPUT") == "true"
) or os.environ.get("MCP_MODE") == "stdio"

if DISABLE_STDOUT:
    # Configure logger to output to stderr only
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class ImmichStdioServer:
    """
    Stdio-based MCP server for Immich API.

    This server handles JSON-RPC communication over stdin/stdout,
    providing MCP tools for interacting with Immich photo management.
    """

    def __init__(self):
        """Initialize the stdio server."""
        self.config: Optional[ImmichConfig] = None
        self.immich_client: Optional[ImmichClient] = None
        self.immich_tools: Optional[ImmichTools] = None
        self.tool_server: Optional[ToolServer] = None
        # stdio server doesn't need to be stored; we'll use mcp.server.stdio.stdio_server context manager
        self._shutdown_event = asyncio.Event()

    async def initialize(self) -> None:
        """Initialize the server components."""
        try:
            # Load configuration
            self.config = load_config()
            logger.info("Configuration loaded successfully")

            # Test connection
            if not await self.config.test_connection():
                raise ValueError("Immich API connection test failed.")

            # Initialize client and tools
            self.immich_client = ImmichClient(self.config)
            self.immich_tools = ImmichTools(self.config)

            # Create and configure the tool server
            self.tool_server = ToolServer(
                name="immich-mcp-server",
                instructions="MCP server for Immich API with tools for pinging, albums, assets, search, and uploads.",
                tools=[
                    # Album and asset management
                    Tool.from_function(self.immich_tools.get_all_albums),
                    Tool.from_function(self.immich_tools.get_album_info),
                    Tool.from_function(self.immich_tools.create_album),
                    Tool.from_function(self.immich_tools.delete_album),
                    Tool.from_function(self.immich_tools.add_assets_to_album),
                    Tool.from_function(self.immich_tools.remove_assets_from_album),
                    # Asset access
                    Tool.from_function(self.immich_tools.get_all_assets),
                    Tool.from_function(self.immich_tools.get_asset_info),
                    Tool.from_function(self.immich_tools.get_person_thumbnail),
                    # Search capabilities
                    Tool.from_function(self.immich_tools.search_metadata),
                    Tool.from_function(self.immich_tools.search_smart),
                    Tool.from_function(self.immich_tools.search_people),
                    Tool.from_function(self.immich_tools.search_places),
                    Tool.from_function(self.immich_tools.get_search_suggestions),
                    Tool.from_function(self.immich_tools.search_random),
                    # People
                    Tool.from_function(self.immich_tools.get_all_people),
                    Tool.from_function(self.immich_tools.get_person),
                    Tool.from_function(self.immich_tools.get_person_statistics),
                ],
            )

            # Note: the stdio transport is provided via mcp.server.stdio.stdio_server
            logger.info(
                "Tool server initialized successfully; stdio transport will be attached at runtime"
            )

        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            raise

    async def run(self) -> None:
        """Run the stdio server."""
        try:
            await self.initialize()

            logger.info("Starting Immich MCP stdio server...")
            # Use the stdio transport which yields read and write streams
            # FastMCP provides its own stdio transport runner. Run it in a separate thread
            # because FastMCP.run is synchronous (it calls anyio.run internally).
            try:
                await asyncio.to_thread(self.tool_server.run, "stdio")
            except Exception:
                logger.error("Exception inside tool_server.run:")
                import traceback

                tb = traceback.format_exc()
                print(tb, file=sys.stderr)
                raise

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        """Shutdown the server gracefully."""
        logger.info("Shutting down server...")

        # No explicit stdio server to close; if tool_server has a shutdown, close it
        if self.tool_server:
            try:
                # tool_server may provide a close/stop API; attempt if available
                close_fn = getattr(self.tool_server, "close", None) or getattr(
                    self.tool_server, "shutdown", None
                )
                if close_fn:
                    if asyncio.iscoroutinefunction(close_fn):
                        await close_fn()
                    else:
                        close_fn()
            except Exception as e:
                logger.error(f"Error closing tool server: {e}")

        # immich_tools is not a context manager; if it exposes a close or shutdown API, call it
        if self.immich_tools:
            try:
                close_tools = getattr(self.immich_tools, "close", None) or getattr(
                    self.immich_tools, "shutdown", None
                )
                if close_tools:
                    if asyncio.iscoroutinefunction(close_tools):
                        await close_tools()
                    else:
                        close_tools()
            except Exception as e:
                logger.error(f"Error closing tools: {e}")

        self._shutdown_event.set()
        logger.info("Server shutdown complete")

    async def wait_for_shutdown(self) -> None:
        """Wait for shutdown signal."""
        await self._shutdown_event.wait()


async def main() -> None:
    """Main entry point for stdio server."""
    server = ImmichStdioServer()

    # Set up signal handlers for graceful shutdown
    import signal

    def signal_handler():
        """Handle shutdown signals."""
        logger.info("Received shutdown signal")
        asyncio.create_task(server.shutdown())

    # Register signal handlers
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, lambda s, f: signal_handler())

    try:
        await server.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
