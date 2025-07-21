
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.fastmcp.tools.base import Tool

load_dotenv()

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
    # Load configuration from environment variables or .env file
    immich_api_url = os.getenv("IMMICH_API_URL")
    immich_api_key = os.getenv("IMMICH_API_KEY")

    if not immich_api_url or not immich_api_key:
        print("Warning: IMMICH_API_URL and IMMICH_API_KEY not set. Immich features will not be available.")
        # Alternatively, you could raise an error or provide mock functionality

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

