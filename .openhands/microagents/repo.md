
# Project Description

This repository appears to be a Model Context Protocol (MCP) server for integrating with the Immich API. It uses FastAPI for the web server and `mcp` for handling tools. The `pyproject.toml` indicates dependencies like `mcp`, `fastapi`, `uvicorn`, and `python-dotenv`. The main purpose is to expose Immich API functionalities as tools through the MCP.

# File Structure

- `pyproject.toml`: Project metadata, dependencies, and build system configuration.
- `README.md`: Basic project README, currently just "# test".
- `src/`: Contains the main application source code.
    - `src/main.py`: The primary entry point for the FastAPI application, setting up the `ToolServer` and mounting it. It defines an `ImmichTools` class with a `get_server_version` tool.
    - `src/immich_mcp/server.py`: Another Python file that seems to define a `create_mcp_server` function and a `GreetTool`. This might be an older or alternative server setup.
- `tests/`: Placeholder for tests.
- `build/`: Build artifacts.
- `immich_mcp.egg-info/`: Python package metadata.

# How to Run Tests or Other Relevant Commands

**To run the server:**

The `src/main.py` file uses Uvicorn. You can run it using:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
or by running the script directly if `uvicorn` is installed:
```bash
python3 src/main.py
```

Ensure all dependencies are installed first:
```bash
pip install -e .
```
This will install `mcp`, `fastapi`, `uvicorn[standard]`, and `python-dotenv`.

**Environment Variables:**

The application uses `python-dotenv` to load environment variables. You will need to set `IMMICH_API_KEY` and `IMMICH_BASE_URL` (defaults to `http://localhost:2283/api`) for the Immich tools to function correctly. You can create a `.env` file in the root directory:
```
IMMICH_API_KEY=your_immich_api_key
IMMICH_BASE_URL=http://your_immich_instance:2283/api
```

**Tests:**

The `tests/` directory is currently empty. There are no tests configured or implemented yet.

# Additional Information

The project aims to be an MCP server for the Immich API, allowing other MCP clients to interact with Immich functionalities as exposed tools. The `src/main.py` seems to be the active server implementation. The `src/immich_mcp/server.py` file might be a remnant or an alternative approach, as `main.py` already defines and exposes `ImmichTools`. A brand new developer should focus on `src/main.py` for understanding the current server setup. The project will likely expand with more Immich-related tools.

