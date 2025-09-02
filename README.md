# Immich MCP Server

This project provides a Model Context Protocol (MCP) server for the Immich photo management system.

## Installation

It is recommended to use a virtual environment.

```bash
pip install .
```

For development, you can install the project with its development dependencies:

```bash
pip install -e ".[dev]"
```

## Running the Server

To run the server for development, you can use the `mcp` command-line tool provided by the `mcp` package. As recommended by the [MCP Python SDK Quickstart](https://github.com/modelcontextprotocol/python-sdk#quickstart), `uv` is the preferred tool for running the server.

First, ensure `uv` is installed:
```bash
pip install uv
```

Then, run the server:

```bash
uv run mcp dev src/immich_mcp/server.py
```

## Configuration

The server requires the following environment variables to be set to connect to your Immich instance:

- `IMMICH_BASE_URL`: The base URL of your Immich instance (e.g., `http://immich.local:2283`). The server will automatically append the required `/api` path.
- `IMMICH_API_KEY`: Your Immich API key.

## Functional Testing

To run the functional tests, see the instructions in `tests/functional/README.md`.
