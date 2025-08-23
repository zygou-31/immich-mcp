# ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Required
IMMICH_BASE_URL=https://your-immich-server.com
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
