# Agent Instructions for `immich-mcp`

This document provides guidance for AI agents working on the `immich-mcp` codebase.

## Project Overview

`immich-mcp` is a server that implements the Model Context Protocol (MCP) for the Immich API. It allows AI assistants to interact with an Immich photo library through a standardized interface, enabling features like intelligent photo management, search, and organization.

The project is built with Python, using FastAPI for the web server and Pydantic for data validation.

## Installation and Setup

To get started with development, you need to set up a virtual environment and install the required dependencies.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/immich-mcp.git
    cd immich-mcp
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The project uses `pip` for dependency management. Install the development dependencies with:
    ```bash
    pip install -e ".[dev]"
    ```

## Configuration

The server is configured via environment variables. Create a `.env` file in the project root by copying the `.env.example` file.

```bash
cp .env.example .env
```

The following environment variables are **required**:

-   `IMMICH_BASE_URL`: The base URL of your Immich server's API (e.g., `https://your-immich-server.com/api`).
-   `IMMICH_API_KEY`: Your Immich API key.
-   `AUTH_TOKEN`: A secret bearer token used to authenticate with the MCP server.

Refer to the `README.md` for a full list of optional configuration variables.

## Running the Server

For development, you can run the server using `uvicorn`, which provides auto-reloading on code changes.

```bash
uvicorn immich_mcp.cli:app --host 0.0.0.0 --port 8626 --reload
```

The server will be available at `http://localhost:8626`. The API documentation can be accessed at `http://localhost:8626/docs`.

## Testing

The project has a comprehensive test suite using `pytest`. To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=immich_mcp --cov-report=html
```

All tests should pass before submitting any changes. New features should be accompanied by new tests.

## Available Tools

The server exposes the Immich API through a set of tools. Here is a summary of the key tools available:

-   **`discover_tools(query: str)`**: Find relevant tools based on a natural language query.
-   **`get_asset_info(asset_id: str, ...)`**: Get detailed information about a specific photo or video.
-   **`search_metadata(...)`**: Search for assets based on metadata like camera model, location, or date.
-   **`search_smart(query: str, ...)`**: Use AI-powered search to find assets based on natural language queries.
-   **`search_people(name: str, ...)`**: Search for people in the photo library.
-   **`get_all_albums(...)`**: Retrieve all albums.
-   **`create_album(album_name: str, ...)`**: Create a new album.
-   **`add_assets_to_album(album_id: str, asset_ids: List[str], ...)`**: Add photos or videos to an album.
-   ... and many more. Refer to the `README.md` for a full list of tools and their parameters.

## Code Style

This project uses `ruff` for code formatting and linting. Before committing any changes, make sure to format and lint your code:

```bash
# Format and lint code
ruff check . --fix && ruff format .
```

This ensures that all code contributed to the project maintains a consistent style.
