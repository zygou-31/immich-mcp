# Immich MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)](https://fastapi.tiangolo.com/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://modelcontextprotocol.io/)

A production-ready Model Context Protocol (MCP) server for the Immich photo management API. This server provides a standardized interface for AI assistants to interact with your Immich photo library, enabling intelligent photo management, search, and organization capabilities.

## 🚀 Features

- **Complete Immich API Integration**: Full access to albums, assets, search, and upload functionality
- **Production-Ready**: Built with caching, rate limiting, and error handling
- **FastAPI Integration**: Modern async web framework with automatic API documentation
- **Comprehensive Testing**: Full test coverage with mocked API responses
- **Environment Configuration**: Flexible configuration via environment variables or .env files
- **Performance Optimized**: Caching and rate limiting for optimal performance
- **Type Safety**: Full type hints and Pydantic validation

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🛠 Installation

### Prerequisites

- Python 3.10 or higher
- Immich server instance (v1.90.0+)
- Immich API key (obtain from your Immich server settings)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Install dependencies
pip install -e .

# Or install from PyPI (when available)
pip install immich-mcp
```

### Development Install

```bash
# Clone and install in development mode
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Required
IMMICH_BASE_URL=https://your-immich-server.com/api
IMMICH_API_KEY=your-api-key-here

# Optional
IMMICH_TIMEOUT=30
IMMICH_MAX_RETRIES=3
```

### Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `IMMICH_BASE_URL` | ✅ | - | Base URL of your Immich server API |
| `IMMICH_API_KEY` | ✅ | - | API key from Immich server settings |
| `IMMICH_TIMEOUT` | ❌ | 30 | HTTP request timeout in seconds |
| `IMMICH_MAX_RETRIES` | ❌ | 3 | Maximum retry attempts for failed requests |

### Getting Your API Key

1. Open your Immich web interface
2. Go to **Settings** → **API Keys**
3. Create a new API key with appropriate permissions
4. Copy the key to your `.env` file

## 🚀 Usage

### Starting the Server

```bash
# Start the server
python -m immich_mcp.server

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000

# With auto-reload for development
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

This project includes a `Dockerfile` and `docker-compose.yml` for easy containerization.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (if using `docker-compose.yml`)

#### Building the Docker Image

To build the Docker image, run the following command from the project root:

```bash
docker build -t immich-mcp .
```

#### Running with Docker

You can run the container using `docker run`. You'll need to provide the required environment variables.

```bash
docker run -d \
  --name immich-mcp-container \
  -p 8000:8000 \
  -e IMMICH_BASE_URL="https://your-immich-server.com/api" \
  -e IMMICH_API_KEY="your-api-key" \
  immich-mcp
```

#### Running with Docker Compose

For a more streamlined experience, you can use Docker Compose.

1.  **Create a `.env` file:**

    Copy the `.env.example` to `.env` and fill in your Immich server details.

    ```bash
    cp .env.example .env
    ```

    Your `.env` file should look like this:

    ```
    IMMICH_BASE_URL=https://your-immich-server.com/api
    IMMICH_API_KEY=your-api-key-here
    ```

2.  **Start the service:**

    Run the following command to build and start the service in detached mode:

    ```bash
    docker-compose up --build -d
    ```

3.  **Stopping the service:**

    To stop the service, run:

    ```bash
    docker-compose down
    ```

## 📖 API Reference

### Available Tools

#### `get_all_assets()`
Retrieves all assets from your Immich library.

**Returns:** JSON string containing array of asset objects

**Example:**
```python
assets = await immich_tools.get_all_assets()
```

#### `get_asset_info(asset_id: str)`
Gets detailed information about a specific asset.

**Parameters:**
- `asset_id` (str): The unique identifier of the asset

**Returns:** JSON string containing asset details

**Example:**
```python
asset_info = await immich_tools.get_asset_info("550e8400-e29b-41d4-a716-446655440000")
```

#### `search_photos(query: str, limit: int = 20, album_id: str = None)`
Searches for photos using smart search.

**Parameters:**
- `query` (str): Search query string
- `limit` (int): Maximum number of results (default: 20)
- `album_id` (str): Optional album ID to search within

**Returns:** JSON string containing search results

**Example:**
```python
results = await immich_tools.search_photos("sunset beach", limit=10)
```

#### `get_all_albums()`
Retrieves all albums from your Immich library.

**Returns:** JSON string containing array of album objects

**Example:**
```python
albums = await immich_tools.get_all_albums()
```

#### `create_album(album_name: str, description: str = "", assets: list = [])`
Creates a new album.

**Parameters:**
- `album_name` (str): Name of the new album
- `description` (str): Optional album description
- `assets` (list): Optional list of asset IDs to include

**Returns:** JSON string containing created album details

**Example:**
```python
album = await immich_tools.create_album("Summer 2024", "Beach vacation photos")
```

#### `upload_photo(file_path: str, album_id: str = None)`
Uploads a new photo to Immich.

**Parameters:**
- `file_path` (str): Path to the photo file
- `album_id` (str): Optional album ID to add the photo to

**Returns:** JSON string containing upload result

**Example:**
```python
result = await immich_tools.upload_photo("/path/to/photo.jpg", album_id="album-uuid")
```

#### `search_metadata(query: str = "", asset_type: str = None, is_favorite: bool = None, limit: int = 100)`
Search assets by metadata criteria.

**Parameters:**
- `query` (str): Search query string for metadata (filename, description, etc.)
- `asset_type` (str): Filter by asset type (IMAGE, VIDEO, AUDIO, OTHER)
- `is_favorite` (bool): Filter by favorite status
- `limit` (int): Maximum number of results to return

**Returns:** JSON string containing search results with assets and total count

**Example:**
```python
results = await tools.search_metadata("beach", "IMAGE", True, 50)
```

#### `search_smart(query: str, limit: int = 100)`
Smart search using AI to find assets based on natural language queries.

**Parameters:**
- `query` (str): Natural language search query (e.g., "photos of my dog at the beach")
- `limit` (int): Maximum number of results to return

**Returns:** JSON string containing AI-powered search results

**Example:**
```python
results = await tools.search_smart("photos of my dog at the beach", 10)
```

#### `search_people(query: str = "", limit: int = 50)`
Search for people in the photo library.

**Parameters:**
- `query` (str): Search query for person names
- `limit` (int): Maximum number of results to return

**Returns:** JSON string containing list of people matching the search criteria

**Example:**
```python
people = await tools.search_people("John", 10)
```

#### `search_places(query: str = "", limit: int = 50)`
Search for places and locations in the photo library.

**Parameters:**
- `query` (str): Search query for place names
- `limit` (int): Maximum number of results to return

**Returns:** JSON string containing list of places matching the search criteria

**Example:**
```python
places = await tools.search_places("beach", 10)
```

#### `get_search_suggestions(query: str = "")`
Get search suggestions based on partial queries.

**Parameters:**
- `query` (str): Partial search query for suggestions

**Returns:** JSON string containing list of search suggestions

**Example:**
```python
suggestions = await tools.get_search_suggestions("be")
```

#### `search_random(limit: int = 10)`
Get random assets from the photo library.

**Parameters:**
- `limit` (int): Maximum number of random assets to return

**Returns:** JSON string containing list of random assets

**Example:**
```python
random_assets = await tools.search_random(5)
```

#### `get_all_people(query: str = "", limit: int = 100, offset: int = 0)`
Get all people from the photo library.

**Parameters:**
- `query` (str): Search query for filtering people by name
- `limit` (int): Maximum number of people to return
- `offset` (int): Number of people to skip for pagination

**Returns:** JSON string containing people list and total count

**Example:**
```python
people = await tools.get_all_people("John", 50, 0)
```

#### `get_person(person_id: str)`
Get detailed information about a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person to retrieve

**Returns:** JSON string containing person details

**Example:**
```python
person = await tools.get_person("550e8400-e29b-41d4-a716-446655440000")
```

#### `get_person_statistics(person_id: str)`
Get statistics for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person

**Returns:** JSON string containing statistics

**Example:**
```python
stats = await tools.get_person_statistics("550e8400-e29b-41d4-a716-446655440000")
```

#### `get_person_thumbnail(person_id: str)`
Get thumbnail image for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person

**Returns:** Base64 encoded thumbnail image data

**Example:**
```python
thumbnail = await tools.get_person_thumbnail("550e8400-e29b-41d4-a716-446655440000")
```

#### `get_all_albums()`
Retrieves all albums from your Immich library.

**Returns:** JSON string containing array of album objects

**Example:**
```python
albums = await immich_tools.get_all_albums()
```

#### `create_album(album_name: str, description: str = "", asset_ids: Optional[List[str]] = None)`
Creates a new album.

**Parameters:**
- `album_name` (str): Name of the new album
- `description` (str): Optional album description
- `asset_ids` (list): Optional list of asset IDs to include

**Returns:** JSON string containing created album details

**Example:**
```python
album = await immich_tools.create_album("Summer 2024", "Beach vacation photos")
```

#### `get_album_info(album_id: str)`
Gets information about a specific album.

**Parameters:**
- `album_id` (str): The unique identifier of the album to retrieve

**Returns:** JSON string containing album details

**Example:**
```python
album = await immich_tools.get_album_info("550e8400-e29b-41d4-a716-446655440000")
```

#### `delete_album(album_id: str)`
Deletes an album from Immich.

**Parameters:**
- `album_id` (str): The unique identifier of the album to delete

**Returns:** JSON string containing status

**Example:**
```python
await immich_tools.delete_album("550e8400-e29b-41d4-a716-446655440000")
```

#### `add_assets_to_album(album_id: str, asset_ids: List[str])`
Adds assets to an existing album.

**Parameters:**
- `album_id` (str): The unique identifier of the album
- `asset_ids` (list): List of asset IDs to add

**Returns:** JSON string containing results

**Example:**
```python
results = await immich_tools.add_assets_to_album("album-uuid", ["asset-uuid-1", "asset-uuid-2"])
```

#### `remove_assets_from_album(album_id: str, asset_ids: List[str])`
Removes assets from an album.

**Parameters:**
- `album_id` (str): The unique identifier of the album
- `asset_ids` (list): List of asset IDs to remove

**Returns:** JSON string containing results

**Example:**
```python
results = await immich_tools.remove_assets_from_album("album-uuid", ["asset-uuid-1", "asset-uuid-2"])
```

### API Endpoints

When running the server, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Development

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Project Structure

```
immich-mcp/
├── immich_mcp/
│   ├── __init__.py
│   ├── client.py          # Immich API client
│   ├── config.py          # Configuration management
│   ├── tools.py           # MCP tools implementation
│   ├── cache.py           # Caching utilities
│   ├── rate_limiter.py    # Rate limiting
│   └── server.py          # FastAPI server
├── tests/
│   ├── __init__.py
│   └── immich_mcp/
│       ├── test_client.py
│       ├── test_config.py
│       └── test_tools.py
├── main.py               # Entry point
├── pyproject.toml        # Project configuration
├── README.md            # This file
└── .env.example         # Environment template
```

### Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8

# Type check
mypy immich_mcp/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=immich_mcp --cov-report=html

# Run specific test file
pytest tests/immich_mcp/test_client.py

# Run with verbose output
pytest -v
```

### Test Structure

Tests are organized in the `tests/` directory:
- `test_client.py`: Tests for the Immich API client
- `test_config.py`: Tests for configuration validation
- `test_tools.py`: Tests for MCP tools functionality

### Writing Tests

Use `respx` for mocking HTTP requests:

```python
import pytest
import respx
import httpx
from immich_mcp.client import ImmichClient

@pytest.mark.asyncio
async def test_example():
    async with respx.mock:
        respx.get("http://test.com/api/assets").mock(
            return_value=httpx.Response(200, json=[{"id": "1"}])
        )
        
        client = ImmichClient(config)
        result = await client.get_all_assets()
        assert len(result) == 1
```

## 🚀 Deployment

### Production Deployment

#### Using Docker

```bash
# Build production image
docker build -t immich-mcp:latest .

# Run with production settings
docker run -d \
  --name immich-mcp \
  -p 8000:8000 \
  -e IMMICH_BASE_URL=https://your-immich-server.com/api \
  -e IMMICH_API_KEY=your-api-key \
  --restart unless-stopped \
  immich-mcp:latest
```

#### Using systemd

Create `/etc/systemd/system/immich-mcp.service`:

```ini
[Unit]
Description=Immich MCP Server
After=network.target

[Service]
Type=exec
User=immich-mcp
WorkingDirectory=/opt/immich-mcp
Environment=IMMICH_BASE_URL=https://your-immich-server.com/api
Environment=IMMICH_API_KEY=your-api-key
ExecStart=/opt/immich-mcp/venv/bin/python -m immich_mcp.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable immich-mcp
sudo systemctl start immich-mcp
```

### Environment-Specific Configuration

#### Development
```bash
# .env.development
IMMICH_BASE_URL=http://localhost:2283/api
IMMICH_API_KEY=dev-key
IMMICH_TIMEOUT=60
```

#### Production
```bash
# .env.production
IMMICH_BASE_URL=https://immich.yourdomain.com/api
IMMICH_API_KEY=production-key
IMMICH_TIMEOUT=30
```

## CI/CD

This project uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/ci.yml` and includes the following jobs:

### Lint & Test

This job runs on every push and pull request to the `main` branch. It performs the following checks:
- Lints the code with `ruff`.
- Checks code formatting with `black`.
- Runs the test suite with `pytest` against multiple Python versions.

### Publish to Docker Hub

This job runs automatically when a new release is created on GitHub. It builds the Docker image and publishes it to [Docker Hub](https://hub.docker.com/r/zygou/immich-mcp).

The image is tagged with the release version (e.g., `v1.0.0`) and `latest`.

#### Configuring Secrets

To allow the workflow to publish to your Docker Hub repository, you need to configure the following secrets in your GitHub repository settings under `Settings` > `Secrets and variables` > `Actions`:

- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: A Docker Hub Personal Access Token (PAT) with read/write permissions.

## 🔧 Troubleshooting

### Common Issues

#### Connection Errors

**Problem**: `Connection test failed`
**Solution**:
1. Verify your `IMMICH_BASE_URL` ends with `/api`
2. Check that your Immich server is accessible
3. Ensure your API key is valid and has proper permissions

```bash
# Test connectivity
curl -H "x-api-key: your-api-key" https://your-immich-server.com/api/server-info/ping
```

#### Authentication Errors

**Problem**: `401 Unauthorized`
**Solution**:
1. Verify your API key is correct
2. Check that the API key has sufficient permissions
3. Ensure the key hasn't expired

#### Rate Limiting

**Problem**: `429 Too Many Requests`
**Solution**:
1. Reduce request frequency
2. Increase rate limit settings in configuration
3. Implement exponential backoff

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python -m immich_mcp.server
```

### Health Checks

The server provides health check endpoints:

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/health/detailed
```

### Performance Monitoring

Monitor server performance:

```bash
# Check memory usage
ps aux | grep immich-mcp

# Monitor logs
tail -f /var/log/immich-mcp.log
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Review [GitHub Issues](https://github.com/your-org/immich-mcp/issues)
3. Enable debug logging for detailed error information
4. Join our [Discord community](https://discord.gg/immich-mcp)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Immich](https://immich.app/) for the amazing photo management platform
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [MCP](https://modelcontextprotocol.io/) for the protocol specification

## 📊 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

**Made with ❤️ by the Immich MCP Team**
