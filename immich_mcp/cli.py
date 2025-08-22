from mcp.server.fastmcp.server import FastMCP as ToolServer
from mcp.server.fastmcp.tools.base import Tool
from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import logging
import contextlib
import os
from contextlib import asynccontextmanager
import inspect

from immich_mcp.client import ImmichClient
from immich_mcp.config import ImmichConfig, load_config
from immich_mcp.tools import ImmichTools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Global variable for config
config: ImmichConfig = None
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """
    global config
    try:
        config = load_config()
        app.state.config = config
        logger.info("Configuration loaded successfully")
        if not await config.test_connection():
            raise ValueError("Immich API connection test failed.")

        # Create and attach the Immich client
        immich_client = ImmichClient(config)
        app.state.immich_client = immich_client

        # Create and attach the tools
        immich_tools = ImmichTools(config)
        app.state.immich_tools = immich_tools

        # Dynamically create tools from ImmichTools methods
        tools = []
        for name, method in inspect.getmembers(
            immich_tools, predicate=inspect.ismethod
        ):
            if not name.startswith("_"):
                tools.append(Tool.from_function(method))

        # Create and mount the tool server
        tool_server = ToolServer(
            name="immich-mcp-server",
            instructions="MCP server for Immich API. To get started, you can use the 'discover_tools' tool with a query to find relevant tools for your task. For example: discover_tools(query='search for photos').",
            tools=tools,
        )

        # Optionally disable mounting the streamable HTTP app (useful for stdio-only tests)
        disable_streamable = (
            "DISABLE_STREAMABLE_HTTP" in os.environ
            and os.environ.get("DISABLE_STREAMABLE_HTTP") == "true"
        )

        if not disable_streamable:
            app.mount("/mcp", tool_server.streamable_http_app())

        # Only start the tool server's session manager if the streamable app is enabled
        if not disable_streamable:
            async with contextlib.AsyncExitStack() as stack:
                await stack.enter_async_context(tool_server.session_manager.run())
                yield
        else:
            # For stdio-only runs/tests, yield without starting HTTP session manager
            yield
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise


# Security scheme
auth_scheme = HTTPBearer()


# Dependency to verify the token
def verify_token(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    config = request.app.state.config
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != config.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        lifespan=lifespan,
    )
    router = APIRouter()
    router.add_api_route(
        "/", lambda: {"message": "Hello World"}, dependencies=[Depends(verify_token)]
    )
    router.add_api_route("/health", lambda: {"status": "ok"})
    app.include_router(router)
    return app


app = create_app()


def main():
    """
    Main entry point for the Immich MCP server.
    This function parses command-line arguments and starts the server
    in the specified mode (HTTP or stdio).
    """
    import argparse
    import asyncio
    import uvicorn

    parser = argparse.ArgumentParser(
        description="Immich MCP server for AI agent integration."
    )
    parser.add_argument(
        "--mode",
        default=os.environ.get("MCP_MODE", "http"),
        help="Mode to run: http or stdio. Defaults to 'http'.",
    )
    args = parser.parse_args()

    mode = args.mode

    if mode == "stdio":
        logger.info("Starting stdio server mode")
        try:
            from immich_mcp.stdio_bridge import main as stdio_main

            asyncio.run(stdio_main())
        except ImportError:
            logger.error("Failed to import stdio_bridge. Make sure it is available.")
            raise
        except Exception as e:
            logger.error(f"An error occurred in stdio mode: {e}")
            raise
    elif mode == "http":
        disable_uvicorn = (
            "DISABLE_UVICORN" in os.environ
            and os.environ.get("DISABLE_UVICORN") == "true"
        )
        # If uvicorn disabled via env, skip starting the HTTP server
        if disable_uvicorn:
            logger.info("Skipping uvicorn.run due to DISABLE_UVICORN=true")
        else:
            logger.info("Starting HTTP server mode")
            uvicorn.run(app, host="0.0.0.0", port=8626)
    else:
        logger.error(f"Invalid mode specified: {mode}. Choose 'http' or 'stdio'.")


if __name__ == "__main__":
    main()
