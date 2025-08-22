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
IMMICH_API_KEY=your-immich-api-key-here
AUTH_TOKEN=your-secret-auth-token-here

# Optional - for loading secrets from files
# AUTH_TOKEN_FILE=/path/to/your/auth_token.secret
# IMMICH_API_KEY_FILE=/path/to/your/immich_api_key.secret

# Optional - for server settings
IMMICH_TIMEOUT=30
IMMICH_MAX_RETRIES=3
MCP_PORT=8626
MCP_BASE_URL=""
```

### Configuration Options

| Variable | Required | Default | Description |
|-----------------------|----------|---------|-----------------------------------------------------------------|
| `IMMICH_BASE_URL` | ✅ | - | Base URL of your Immich server API |
| `IMMICH_API_KEY` | ✅ | - | API key from Immich server settings (or use `IMMICH_API_KEY_FILE`) |
| `AUTH_TOKEN` | ✅ | - | Bearer token for authenticating with the MCP server (or use `AUTH_TOKEN_FILE`) |
| `IMMICH_API_KEY_FILE` | ❌ | - | Path to a file containing the Immich API key |
| `AUTH_TOKEN_FILE` | ❌ | - | Path to a file containing the auth token |
| `IMMICH_TIMEOUT` | ❌ | 30 | HTTP request timeout in seconds |
| `IMMICH_MAX_RETRIES` | ❌ | 3 | Maximum retry attempts for failed requests |
| `MCP_PORT` | ❌ | 8626 | Port to run the MCP server on |
| `MCP_BASE_URL` | ❌ | "" | Base URL (subpath) for reverse proxy setups |

### Security

The MCP server is protected by a bearer token. You must provide the `AUTH_TOKEN` in your requests via the `Authorization` header.

Example:
```bash
curl -H "Authorization: Bearer your-secret-auth-token-here" \
     http://localhost:8626/
```

### Getting Your Immich API Key

1. Open your Immich web interface
2. Go to **Settings** → **API Keys**
3. Create a new API key with appropriate permissions
4. Copy the key to your `.env` file

## 🚀 Usage

### Starting the Server

Once installed, you can start the server with the following command:

```bash
immich-mcp
```

This will start the server on `http://0.0.0.0:8626`.

You can also run the server in stdio mode:

```bash
immich-mcp --mode stdio
```

For development, you can use `uvicorn` for auto-reloading:

```bash
uvicorn immich_mcp.cli:app --host 0.0.0.0 --port 8626 --reload
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
  -p 8626:8626 \
  -e IMMICH_BASE_URL="https://your-immich-server.com/api" \
  -e IMMICH_API_KEY="your-immich-api-key" \
  -e AUTH_TOKEN="your-secret-auth-token" \
  -e MCP_PORT="8626" \
  -e MCP_BASE_URL="/mcp" \
  immich-mcp
```

*Note: `MCP_PORT` and `MCP_BASE_URL` are optional.*

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
    AUTH_TOKEN=your-secret-auth-token-here
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

#### `discover_tools(query: str)`
Discovers relevant tools based on a natural language query.

**Parameters:**
- `query` (str): A natural language query describing the desired functionality.

**Returns:** A JSON string containing a list of recommended tools, including their names and descriptions.

#### `get_asset_info(asset_id: str, key: Optional[str] = None, slug: Optional[str] = None)`
Gets detailed information about a specific asset.

**Parameters:**
- `asset_id` (str): The unique identifier of the asset.
- `key` (str, optional): The key for the asset, used for shared links.
- `slug` (str, optional): The slug for the asset, used for shared links.

**Returns:** JSON string containing asset details.

#### `search_metadata(...)`
Search assets by metadata criteria. This tool accepts a large number of optional parameters based on the Immich API.

**Example Parameters:**
- `is_favorite: bool = True`
- `city: str = "London"`
- `person_ids: List[str] = ["..."]`
- ... and many more. See the tool's docstring for a full list.

**Returns:** JSON string containing search results.

#### `search_smart(...)`
Smart search using AI to find assets based on natural language queries.

**Parameters:**
- `query` (str): Natural language search query.
- ... and many other optional filter parameters. See the tool's docstring.

**Returns:** JSON string containing AI-powered search results.

#### `search_people(name: str, with_hidden: Optional[bool] = None)`
Search for people in the photo library.

**Parameters:**
- `name` (str): The name of the person to search for.
- `with_hidden` (bool, optional): Whether to include hidden people in the results.

**Returns:** JSON string containing a list of people.

#### `search_places(name: str)`
Search for places and locations in the photo library.

**Parameters:**
- `name` (str): The name of the place to search for.

**Returns:** JSON string containing a list of places.

#### `get_search_suggestions(...)`
Get search suggestions based on partial queries.

**Parameters:**
- `type` (str): The type of suggestion to get (e.g., "CITY", "MAKE").
- ... and other optional filter parameters. See the tool's docstring.

**Returns:** JSON string containing a list of suggestions.

#### `search_random(...)`
Get random assets from the photo library, with optional filters.

**Example Parameters:**
- `size: int = 10`
- `is_favorite: bool = True`
- ... and many more. See the tool's docstring.

**Returns:** JSON string containing a list of random assets.

#### `get_all_people(...)`
Get all people from the photo library, with optional filters.

**Example Parameters:**
- `page: int = 1`
- `with_hidden: bool = False`
- ... and other optional parameters. See the tool's docstring.

**Returns:** JSON string containing a list of people.

#### `get_person(person_id: str)`
Get detailed information about a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** JSON string containing person details.

#### `get_person_statistics(person_id: str)`
Get statistics for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** JSON string containing statistics.

#### `get_person_thumbnail(person_id: str)`
Get a thumbnail image for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** Base64 encoded thumbnail image data.

#### `get_all_albums(asset_id: Optional[str] = None, shared: Optional[bool] = None)`
Retrieves all albums from your Immich library.

**Parameters:**
- `asset_id` (str, optional): Filter albums containing this asset.
- `shared` (bool, optional): Filter for shared or non-shared albums.

**Returns:** JSON string containing an array of album objects.

#### `create_album(album_name: str, description: str = "", asset_ids: Optional[List[str]] = None, album_users: Optional[List[Dict[str, List[str]]]] = None)`
Creates a new album.

**Parameters:**
- `album_name` (str): Name of the new album.
- `description` (str, optional): Album description.
- `asset_ids` (list, optional): List of asset IDs to include.
- `album_users` (list, optional): List of users to share with.

**Returns:** JSON string containing created album details.

#### `get_album_info(album_id: str, key: Optional[str] = None, slug: Optional[str] = None, without_assets: Optional[bool] = None)`
Gets information about a specific album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `key` (str, optional): Key for shared links.
- `slug` (str, optional): Slug for shared links.
- `without_assets` (bool, optional): Exclude asset information.

**Returns:** JSON string containing album details.

#### `delete_album(album_id: str)`
Deletes an album from Immich.

**Parameters:**
- `album_id` (str): The unique identifier of the album to delete.

**Returns:** JSON string containing status.

#### `add_assets_to_album(album_id: str, asset_ids: List[str], key: Optional[str] = None, slug: Optional[str] = None)`
Adds assets to an existing album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `asset_ids` (list): List of asset IDs to add.
- `key` (str, optional): Key for shared links.
- `slug` (str, optional): Slug for shared links.

**Returns:** JSON string containing results.

#### `remove_assets_from_album(album_id: str, asset_ids: List[str])`
Removes assets from an album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `asset_ids` (list): List of asset IDs to remove.

**Returns:** JSON string containing results.

#### `search_memories(for_date: Optional[str] = None, is_saved: Optional[bool] = None, is_trashed: Optional[bool] = None, memory_type: Optional[str] = None)`
Search for memories.

**Parameters:**
- `for_date` (str, optional): The date to search for memories for.
- `is_saved` (bool, optional): Whether to search for saved memories.
- `is_trashed` (bool, optional): Whether to search for trashed memories.
- `memory_type` (str, optional): The type of memory to search for.

**Returns:** JSON string containing a list of memories.

#### `create_memory(memory_data: Dict[str, Any])`
Create a new memory.

**Parameters:**
- `memory_data` (dict): The data for the new memory.

**Returns:** JSON string containing the created memory.

#### `get_memory_statistics(for_date: Optional[str] = None, is_saved: Optional[bool] = None, is_trashed: Optional[bool] = None, memory_type: Optional[str] = None)`
Get memory statistics.

**Parameters:**
- `for_date` (str, optional): The date to get statistics for.
- `is_saved` (bool, optional): Whether to get statistics for saved memories.
- `is_trashed` (bool, optional): Whether to get statistics for trashed memories.
- `memory_type` (str, optional): The type of memory to get statistics for.

**Returns:** JSON string containing the memory statistics.

#### `get_memory(memory_id: str)`
Get a specific memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.

**Returns:** JSON string containing the memory.

#### `update_memory(memory_id: str, memory_data: Dict[str, Any])`
Update a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `memory_data` (dict): The data to update the memory with.

**Returns:** JSON string containing the updated memory.

#### `delete_memory(memory_id: str)`
Delete a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.

**Returns:** JSON string containing the status of the operation.

#### `add_memory_assets(memory_id: str, asset_ids: List[str])`
Add assets to a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `asset_ids` (list): The IDs of the assets to add.

**Returns:** JSON string containing the response from the server.

#### `remove_memory_assets(memory_id: str, asset_ids: List[str])`
Remove assets from a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `asset_ids` (list): The IDs of the assets to remove.

**Returns:** JSON string containing the response from the server.

### Users (admin)

#### `search_users_admin(user_id: Optional[str] = None, with_deleted: Optional[bool] = None)`
Search for users with admin privileges.

**Parameters:**
- `user_id` (str, optional): The ID of the user to search for.
- `with_deleted` (bool, optional): Whether to include deleted users in the results.

**Returns:** JSON string containing a list of users.

#### `create_user_admin(user_data: Dict[str, Any])`
Create a new user with admin privileges.

**Parameters:**
- `user_data` (dict): The data for the new user.

**Returns:** JSON string containing the created user.

#### `get_user_admin(user_id: str)`
Get detailed information about a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user to retrieve.

**Returns:** JSON string containing user details.

#### `update_user_admin(user_id: str, user_data: Dict[str, Any])`
Update a user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to update.
- `user_data` (dict): The data to update the user with.

**Returns:** JSON string containing the updated user.

#### `delete_user_admin(user_id: str, force: bool = False)`
Delete a user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to delete.
- `force` (bool, optional): Whether to force the deletion.

**Returns:** JSON string containing the deleted user.

#### `get_user_preferences_admin(user_id: str)`
Get preferences for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user.

**Returns:** JSON string containing the user's preferences.

#### `update_user_preferences_admin(user_id: str, preferences_data: Dict[str, Any])`
Update preferences for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user.
- `preferences_data` (dict): The data to update the preferences with.

**Returns:** JSON string containing the updated preferences.

#### `restore_user_admin(user_id: str)`
Restore a deleted user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to restore.

**Returns:** JSON string containing the restored user.

#### `get_user_statistics_admin(user_id: str, is_favorite: Optional[bool] = None, is_trashed: Optional[bool] = None, visibility: Optional[str] = None)`
Get statistics for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user.
- `is_favorite` (bool, optional): Whether to filter by favorite status.
- `is_trashed` (bool, optional): Whether to filter by trashed status.
- `visibility` (str, optional): The visibility of the assets.

**Returns:** JSON string containing the user's statistics.

### Users

#### `search_users()`
Search for users.

**Returns:** JSON string containing a list of users.

#### `get_my_user()`
Get the current user's information.

**Returns:** JSON string containing the current user's information.

#### `update_my_user(user_data: Dict[str, Any])`
Update the current user's information.

**Parameters:**
- `user_data` (dict): The data to update the user with.

**Returns:** JSON string containing the updated user information.

#### `get_user(user_id: str)`
Get a user's information.

**Parameters:**
- `user_id` (str): The ID of the user to retrieve.

**Returns:** JSON string containing the user's information.

#### `delete_user_license()`
Delete the current user's license.

**Returns:** JSON string containing the status of the operation.

#### `get_user_license()`
Get the current user's license.

**Returns:** JSON string containing the user's license.

#### `set_user_license(license_key: str)`
Set the current user's license.

**Parameters:**
- `license_key` (str): The license key to set.

**Returns:** JSON string containing the user's license.

#### `delete_user_onboarding()`
Delete the current user's onboarding status.

**Returns:** JSON string containing the status of the operation.

#### `get_user_onboarding()`
Get the current user's onboarding status.

**Returns:** JSON string containing the user's onboarding status.

#### `set_user_onboarding(onboarding_data: Dict[str, Any])`
Set the current user's onboarding status.

**Parameters:**
- `onboarding_data` (dict): The onboarding data to set.

**Returns:** JSON string containing the user's onboarding status.

#### `get_my_preferences()`
Get the current user's preferences.

**Returns:** JSON string containing the user's preferences.

#### `update_my_preferences(preferences_data: Dict[str, Any])`
Update the current user's preferences.

**Parameters:**
- `preferences_data` (dict): The preferences to update.

**Returns:** JSON string containing the updated preferences.

#### `delete_profile_image()`
Delete the current user's profile image.

**Returns:** JSON string containing the status of the operation.

#### `create_profile_image(file_path: str)`
Create a profile image for the current user.

**Parameters:**
- `file_path` (str): The path to the image file.

**Returns:** JSON string containing the response from the server.

#### `get_profile_image(user_id: str)`
Get a user's profile image.

**Parameters:**
- `user_id` (str): The ID of the user.

**Returns:** Base64 encoded profile image data.

### API Keys

#### `get_api_keys()`
Get all API keys.

**Returns:** JSON string containing a list of API keys.

#### `create_api_key(key_data: Dict[str, Any])`
Create a new API key.

**Parameters:**
- `key_data` (dict): The data for the new API key.

**Returns:** JSON string containing the created API key.

#### `get_api_key(key_id: str)`
Get an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to retrieve.

**Returns:** JSON string containing the API key.

#### `update_api_key(key_id: str, key_data: Dict[str, Any])`
Update an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to update.
- `key_data` (dict): The data to update the API key with.

**Returns:** JSON string containing the updated API key.

#### `delete_api_key(key_id: str)`
Delete an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to delete.

**Returns:** JSON string containing the status of the operation.

### Authentication

#### `sign_up_admin(user_data: Dict[str, Any])`
Sign up a new admin user.

**Parameters:**
- `user_data` (dict): The data for the new admin user.

**Returns:** JSON string containing the created admin user.

#### `change_password(password_data: Dict[str, Any])`
Change the current user's password.

**Parameters:**
- `password_data` (dict): The data for changing the password.

**Returns:** JSON string containing the response from the server.

#### `login(login_data: Dict[str, Any])`
Log in a user.

**Parameters:**
- `login_data` (dict): The data for logging in.

**Returns:** JSON string containing the response from the server.

#### `logout()`
Log out the current user.

**Returns:** JSON string containing the response from the server.

#### `reset_pin_code(pin_code_data: Dict[str, Any])`
Reset the current user's pin code.

**Parameters:**
- `pin_code_data` (dict): The data for resetting the pin code.

**Returns:** JSON string containing the status of the operation.

#### `setup_pin_code(pin_code_data: Dict[str, Any])`
Set up a pin code for the current user.

**Parameters:**
- `pin_code_data` (dict): The data for setting up the pin code.

**Returns:** JSON string containing the status of the operation.

#### `change_pin_code(pin_code_data: Dict[str, Any])`
Change the current user's pin code.

**Parameters:**
- `pin_code_data` (dict): The data for changing the pin code.

**Returns:** JSON string containing the status of the operation.

#### `lock_auth_session()`
Lock the current user's authentication session.

**Returns:** JSON string containing the status of the operation.

#### `unlock_auth_session(unlock_data: Dict[str, Any])`
Unlock the current user's authentication session.

**Parameters:**
- `unlock_data` (dict): The data for unlocking the session.

**Returns:** JSON string containing the status of the operation.

#### `get_auth_status()`
Get the authentication status of the current user.

**Returns:** JSON string containing the authentication status.

#### `validate_access_token()`
Validate the current access token.

**Returns:** JSON string containing the validation status.

### Faces

#### `get_faces(asset_id: str)`
Get all faces for a given asset.

**Parameters:**
- `asset_id` (str): The ID of the asset.

**Returns:** JSON string containing a list of faces.

#### `create_face(face_data: Dict[str, Any])`
Create a new face.

**Parameters:**
- `face_data` (dict): The data for the new face.

**Returns:** JSON string containing the created face.

#### `delete_face(face_id: str)`
Delete a face.

**Parameters:**
- `face_id` (str): The ID of the face to delete.

**Returns:** JSON string containing the status of the operation.

#### `reassign_faces_by_id(face_id: str, person_id: str)`
Reassign a face to a person.

**Parameters:**
- `face_id` (str): The ID of the face to reassign.
- `person_id` (str): The ID of the person to reassign the face to.

**Returns:** JSON string containing the updated person.

### People

#### `create_person(person_data: Dict[str, Any])`
Create a new person.

**Parameters:**
- `person_data` (dict): The data for the new person.

**Returns:** JSON string containing the created person.

#### `update_people(people_data: Dict[str, Any])`
Update people.

**Parameters:**
- `people_data` (dict): The data for updating people.

**Returns:** JSON string containing the updated people.

#### `delete_people(people_data: Dict[str, Any])`
Delete people.

**Parameters:**
- `people_data` (dict): The data for deleting people.

**Returns:** JSON string containing the status of the operation.

#### `update_person(person_id: str, person_data: Dict[str, Any])`
Update a person.

**Parameters:**
- `person_id` (str): The ID of the person to update.
- `person_data` (dict): The data to update the person with.

**Returns:** JSON string containing the updated person.

#### `delete_person(person_id: str)`
Delete a person.

**Parameters:**
- `person_id` (str): The ID of the person to delete.

**Returns:** JSON string containing the status of the operation.

#### `merge_person(person_id: str, merge_data: Dict[str, Any])`
Merge a person.

**Parameters:**
- `person_id` (str): The ID of the person to merge.
- `merge_data` (dict): The data for merging the person.

**Returns:** JSON string containing the response from the server.

#### `reassign_faces(person_id: str, reassign_data: Dict[str, Any])`
Reassign faces to a person.

**Parameters:**
- `person_id` (str): The ID of the person to reassign faces to.
- `reassign_data` (dict): The data for reassigning faces.

**Returns:** JSON string containing the updated people.

### Shared Links

#### `get_all_shared_links()`
Get all shared links.

**Returns:** JSON string containing a list of shared links.

#### `create_shared_link(link_data: Dict[str, Any])`
Create a new shared link.

**Parameters:**
- `link_data` (dict): The data for the new shared link.

**Returns:** JSON string containing the created shared link.

#### `get_my_shared_link()`
Get the current user's shared link.

**Returns:** JSON string containing the current user's shared link.

#### `get_shared_link_by_id(link_id: str)`
Get a shared link by ID.

**Parameters:**
- `link_id` (str): The ID of the shared link to retrieve.

**Returns:** JSON string containing the shared link.

#### `remove_shared_link(link_id: str)`
Remove a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link to remove.

**Returns:** JSON string containing the status of the operation.

#### `update_shared_link(link_id: str, link_data: Dict[str, Any])`
Update a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link to update.
- `link_data` (dict): The data to update the shared link with.

**Returns:** JSON string containing the updated shared link.

#### `remove_shared_link_assets(link_id: str, asset_ids: List[str])`
Remove assets from a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link.
- `asset_ids` (list): The IDs of the assets to remove.

**Returns:** JSON string containing the response from the server.

#### `add_shared_link_assets(link_id: str, asset_ids: List[str])`
Add assets to a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link.
- `asset_ids` (list): The IDs of the assets to add.

**Returns:** JSON string containing the response from the server.

### API Endpoints

When running the server, you can access:

- **Interactive API Docs**: http://localhost:8626/docs
- **ReDoc Documentation**: http://localhost:8626/redoc
- **Health Check**: http://localhost:8626/health

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
├── immich_mcp/
│   ├── cli.py             # Command-line interface
├── pyproject.toml        # Project configuration
├── README.md            # This file
└── .env.example         # Environment template
```

### Code Style

This project uses:
- **ruff** for code formatting and linting
- **mypy** for type checking

```bash
# Format and lint code
ruff check . --fix && ruff format .

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
  -p 8626:8626 \
  -e IMMICH_BASE_URL=https://your-immich-server.com/api \
  -e IMMICH_API_KEY=your-api-key \
  -e MCP_PORT="8626" \
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

### Reverse Proxy Setup

If you want to run the Immich MCP server behind a reverse proxy under a subpath (e.g., `https://your-domain.com/mcp`), you can use the `MCP_BASE_URL` environment variable.

Set `MCP_BASE_URL` to the desired subpath, for example, `/mcp`.

#### Docker Compose with Caddy

Here's an example of how to use it with Caddy as a reverse proxy in a `docker-compose.yml` file.

1.  **Update your `.env` file:**

    Add `MCP_BASE_URL` to your `.env` file:

    ```
    IMMICH_BASE_URL=https://your-immich-server.com/api
    IMMICH_API_KEY=your-api-key-here
    MCP_PORT=8626
    MCP_BASE_URL=/mcp
    ```

2.  **Update your `docker-compose.yml`:**

    Add a Caddy service to your `docker-compose.yml` and make sure both services are on the same network.

    ```yaml
    version: '3.8'

    services:
      immich-mcp:
        build: .
        env_file: .env
        restart: unless-stopped
        networks:
          - mcp-net

      caddy:
        image: caddy:2-alpine
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - ./Caddyfile:/etc/caddy/Caddyfile
          - caddy_data:/data
          - caddy_config:/config
        networks:
          - mcp-net

    networks:
      mcp-net:

    volumes:
      caddy_data:
      caddy_config:
    ```

3.  **Create a `Caddyfile`:**

    Create a file named `Caddyfile` in the same directory with the following content:

    ```
    your-domain.com {
        handle_path /mcp/* {
            reverse_proxy immich-mcp:8626 {
                header_up Host {host}
                header_up X-Real-IP {remote_ip}
                header_up X-Forwarded-For {remote_ip}
                header_up X-Forwarded-Proto {scheme}
            }
        }

        # Other services you might be running
    }
    ```

With this setup, the Immich MCP server will be available at `https://your-domain.com/mcp`, and the API documentation will be correctly served at `https://your-domain.com/mcp/docs`.

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
