# Immich MCP Server

This project provides a [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/specification) server for the [Immich](https://immich.app/) photo management system. It allows you to interact with your Immich instance using MCP-compatible clients.

## Features

The server exposes the following MCP resources and tools:

### Resources

- **`user://me`**: Get details about the current user.
- **`users://list`**: Get a list of all users on the Immich instance.
- **`partners://list`**: Get a list of all partners.
- **`asset://{asset_id}`**: Get details for a specific asset (photo or video) by its ID.
- **`apikey://me`**: Get details about the API key currently being used.
- **`apikeys://list`**: Get a list of all API keys.
- **`apikey://{api_key_id}`**: Get details for a specific API key by its ID.

### Tools

- **`ping()`**: A simple tool to check if the server can successfully connect to the Immich instance. Returns `"pong"` on success.

## Deployment (Recommended)

The easiest way to deploy the Immich MCP server is by using Docker. A `docker-compose.yml` file is provided for your convenience.

1.  **Create a `.env` file:**
    Copy the provided `.env.example` to a new file named `.env`:
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file to set the required environment variables.

2.  **Run the server:**
    ```bash
    docker-compose up -d
    ```
    The server will be available at `http://localhost:8000`.

You can view the server logs with:
```bash
docker-compose logs -f
```

Official container images are available on [Docker Hub](https://hub.docker.com/r/bflad/immich-mcp) and [ghcr.io](https://ghcr.io/bflad/immich-mcp).

## Configuration

The server is configured using environment variables:

| Variable | Description | Default | Required |
| --- | --- | --- | --- |
| `IMMICH_BASE_URL` | The base URL of your Immich instance (e.g., `http://immich.local:2283`). | | **Yes** |
| `IMMICH_API_KEY` | Your Immich API key. | | **Yes** |
| `IMMICH_MCP_PORT` | The port on which the server will listen. | `8626` | No |
| `IMMICH_MCP_TIMEOUT` | The keep-alive timeout for the server in seconds. | `5` | No |
| `TZ` | Sets the timezone inside the container to ensure timestamps are correct. | `UTC` | No |

**Note on `TZ`**: While the application does not directly use this variable, it is a standard in containerized environments to ensure that any timestamps (e.g., in logs) are correctly aligned with your local time.

When running with `docker-compose`, these variables are loaded from the `.env` file.

## Installation (for Development)

For development purposes, you can install and run the server locally.

It is recommended to use a virtual environment.

```bash
# Install the package in editable mode with development dependencies
pip install -e ".[dev]"
```

### Running the Development Server

The recommended way to run the development server is with `uv`:

```bash
# First, ensure uv is installed
pip install uv

# Run the server
uv run mcp dev src/immich_mcp/server.py
```

## For Developers

- The MCP initialization handshake is documented in `docs/INITIALIZATION.md`.
- Functional tests that run against a real Immich instance are documented in `tests/functional/README.md`.
