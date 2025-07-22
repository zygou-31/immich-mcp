


import logging
from mcp.server import Server
from mcp.server.fastmcp.tools.base import Tool
from immich_mcp.config import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a simple tool
class GreetTool(Tool):
    def __init__(self):
        super().__init__(
            name="greet",
            description="Greets the user with a personalized message.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person to greet."
                    }
                },
                "required": ["name"]
            }
        )

    def run(self, name: str):
        return f"Hello, {name}!"

def create_mcp_server() -> Server:
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
            logger.warning("Could not connect to Immich API - functionality may be limited")

    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise

    server = Server(name="Immich MCP Server")
    server.register_tool(GreetTool())

    # Initialize Immich client here with loaded config
    # For now, just a placeholder

    return server

if __name__ == "__main__":
    server = create_mcp_server()
    print("Starting MCP server...")
    # In a real application, you would run this with a proper ASGI server like uvicorn
    # For demonstration, we'll keep it simple or show how to run it

    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8000)

