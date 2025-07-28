# Immich MCP Server

This project is a production-ready Model Context Protocol (MCP) server for the Immich photo management API. It provides a standardized interface for AI assistants to interact with an Immich photo library, enabling intelligent photo management, search, and organization capabilities.

## File Structure

The project is organized as follows:

- `immich_mcp/`: Contains the core application logic.
  - `client.py`: The Immich API client, responsible for making requests to the Immich server.
  - `config.py`: Configuration management, loading settings from environment variables.
  - `tools.py`: The MCP tools implementation, defining the functions available to the AI assistant.
  - `server.py`: The FastAPI server, which exposes the MCP tools as a web API.
- `tests/`: Contains the test suite for the project.
- `main.py`: The entry point for running the server.
- `pyproject.toml`: The project configuration file, including dependencies.
- `README.md`: The main documentation file for the project.

## Running Tests

To run the test suite, use the following command:

```bash
pytest
```

## Running the Server

To run the MCP server, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Other Information

- The server uses `python-dotenv` to manage environment variables. You can create a `.env` file in the project root to store your Immich API key and other settings.
- The server uses `respx` for mocking HTTP requests in the test suite. This allows for testing the API client without making actual requests to an Immich server.
