import logging
from mcp.server.fastmcp import FastMCP
from immich_mcp.config import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mcp_server() -> FastMCP:
    """
    Creates and configures the MCP server for Immich.
    """
    # Load and validate configuration
    try:
        config = load_config()
        logger.info("Immich API configuration loaded")

        # Test connection during startup (async context required)
        import asyncio

        if asyncio.run(config.test_connection()):
            logger.info("Successfully connected to Immich API")
        else:
            logger.warning(
                "Could not connect to Immich API - functionality may be limited"
            )

    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise

    # Create FastMCP server
    server = FastMCP(name="Immich MCP Server")

    # Register a simple tool
    @server.tool()
    def greet(name: str) -> str:
        """Greets the user with a personalized message."""
        return f"Hello, {name}!"

    # Initialize Immich client here with loaded config
    # For now, just a placeholder

    return server


if __name__ == "__main__":
    server = create_mcp_server()
    print("Starting MCP server...")
    # Run the server using stdio transport
    server.run("stdio")
