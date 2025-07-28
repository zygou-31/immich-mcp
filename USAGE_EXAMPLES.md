
# Immich MCP Server - Usage Examples

This document provides comprehensive usage examples for the Immich MCP server, covering common use cases and integration patterns.

## Table of Contents
- [Basic Usage](#basic-usage)
- [Python Integration](#python-integration)
- [MCP Client Examples](#mcp-client-examples)
- [Advanced Usage](#advanced-usage)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)

## Basic Usage

### Starting the Server

```bash
# Quick start with environment variables
export IMMICH_BASE_URL=https://your-immich-server.com/api
export IMMICH_API_KEY=your-api-key
python -m immich_mcp.server

# Using .env file
cp .env.example .env
# Edit .env with your values
python -m immich_mcp.server
```

### Health Check

```bash
# Check if server is running
curl http://localhost:8000/health

# Check API documentation
open http://localhost:8000/docs
```

## Python Integration

### Direct Client Usage

```python
import asyncio
from immich_mcp.client import ImmichClient
from immich_mcp.config import ImmichConfig

async def basic_example():
    # Configure client
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    # Create client
    client = ImmichClient(config)
    
    # Get all assets
    assets = await client.get_all_assets()
    print(f"Total assets: {len(assets)}")
    
    # Get specific asset info
    if assets:
        asset_id = assets[0]["id"]
        asset_info = await client.get_asset(asset_id)
        print(f"First asset: {asset_info['originalFileName']}")

# Run example
if __name__ == "__main__":
    asyncio.run(basic_example())
```

### Using the Tools Class

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def tools_example():
    # Configure
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    # Use tools with async context manager
    async with ImmichTools(config) as tools:
        # Get all assets
        assets_json = await tools.get_all_assets()
        assets = json.loads(assets_json)
        print(f"Found {len(assets)} assets")
        
        # Get asset info
        if assets:
            asset_id = assets[0]["id"]
            asset_info_json = await tools.get_asset_info(asset_id)
            asset_info = json.loads(asset_info_json)
            print(f"Asset name: {asset_info['originalFileName']}")

asyncio.run(tools_example())
```

## MCP Client Examples

### Using with Claude Desktop

1. **Install Claude Desktop**
2. **Configure MCP Server**

Create `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "immich": {
      "command": "python",
      "args": ["-m", "immich_mcp.server"],
      "env": {
        "IMMICH_BASE_URL": "https://your-immich-server.com/api",
        "IMMICH_API_KEY": "your-api-key"
      }
    }
  }
}
```

3. **Usage in Claude**
```
User: Show me my recent photos
Claude: I'll search for your recent photos using the Immich MCP server.
[Uses search_photos tool with query "recent"]
```

### Using with Custom MCP Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def mcp_client_example():
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "immich_mcp.server"],
        env={
            "IMMICH_BASE_URL": "https://your-immich-server.com/api",
            "IMMICH_API_KEY": "your-api-key"
        }
    )
    
    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools])
            
            # Use search tool
            result = await session.call_tool(
                "search_photos",
                arguments={"query": "sunset", "limit": 5}
            )
            print("Search results:", result)

asyncio.run(mcp_client_example())
```

## Advanced Usage

### Batch Operations

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def batch_operations():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # Get all assets
        assets_json = await tools.get_all_assets()
        assets = json.loads(assets_json)
        
        # Process in batches
        batch_size = 50
        for i in range(0, len(assets), batch_size):
            batch = assets[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1}")
            
            # Process each asset in batch
            for asset in batch:
                asset_id = asset["id"]
                asset_info = json.loads(await tools.get_asset_info(asset_id))
                
                # Example: Check for GPS data
                if "exifInfo" in asset_info and asset_info["exifInfo"].get("latitude"):
                    print(f"Asset {asset['originalFileName']} has GPS data")

asyncio.run(batch_operations())
```

### Album Management

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def album_management():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # Create a new album
        album_result = json.loads(
            await tools.create_album(
                album_name="Summer Vacation 2024",
                description="Photos from our summer trip to Hawaii"
            )
        )
        album_id = album_result["id"]
        print(f"Created album: {album_result['albumName']}")
        
        # Search for vacation photos
        vacation_photos = json.loads(
            await tools.search_photos("beach vacation", limit=20)
        )
        
        # Add photos to album (if supported by API)
        # This would require additional API calls

asyncio.run(album_management())
```

### Smart Search Integration

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def smart_search():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # Search by content
        results = json.loads(await tools.search_photos("dog", limit=10))
        print(f"Found {len(results)} photos with dogs")
        
        # Search by location
        beach_photos = json.loads(await tools.search_photos("beach", limit=15))
        print(f"Found {len(beach_photos)} beach photos")
        
        # Search within specific album
        # First get albums
        albums = json.loads(await tools.get_all_albums())
        if albums:
            vacation_album = next((a for a in albums if "vacation" in a["albumName"].lower()), None)
            if vacation_album:
                vacation_photos = json.loads(
                    await tools.search_photos("sunset", album_id=vacation_album["id"], limit=10)
                )
                print(f"Found {len(vacation_photos)} sunset photos in vacation album")

asyncio.run(smart_search())
```

## Error Handling

### Comprehensive Error Handling

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def error_handling_example():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    try:
        async with ImmichTools(config) as tools:
            # Handle invalid asset ID
            try:
                result = json.loads(await tools.get_asset_info("invalid-uuid"))
                if "error" in result:
                    logger.error(f"Error getting asset: {result['error']}")
                else:
                    logger.info(f"Asset found: {result.get('originalFileName')}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                
    except Exception as e:
        logger.error(f"Failed to initialize tools: {e}")

asyncio.run(error_handling_example())
```

### Connection Testing

```python
import asyncio
from immich_mcp.config import ImmichConfig

async def test_connection():
    try:
        config = ImmichConfig(
            immich_base_url="https://your-immich-server.com/api",
            immich_api_key="your-api-key"
        )
        
        # Test connection
        if await config.test_connection():
            print("✅ Connection successful")
        else:
            print("❌ Connection failed")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")

asyncio.run(test_connection())
```

## Performance Optimization

### Caching Strategy

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def caching_example():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # First call - will cache results
        start_time = asyncio.get_event_loop().time()
        assets1 = json.loads(await tools.get_all_assets())
        first_call_time = asyncio.get_event_loop().time() - start_time
        
        # Second call - should use cache
        start_time = asyncio.get_event_loop().time()
        assets2 = json.loads(await tools.get_all_assets())
        second_call_time = asyncio.get_event_loop().time() - start_time
        
        print(f"First call: {first_call_time:.2f}s")
        print(f"Second call: {second_call_time:.2f}s")
        print(f"Speedup: {first_call_time/second_call_time:.1f}x")

asyncio.run(caching_example())
```

### Rate Limiting

```python
import asyncio
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def rate_limiting_example():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # Make multiple requests with rate limiting
        tasks = []
        for i in range(10):
            task = tools.get_all_assets()
            tasks.append(task)
        
        # Execute all requests
        results = await asyncio.gather(*tasks)
        
        # Process results
        for i, result_json in enumerate(results):
            result = json.loads(result_json)
            if "error" not in result:
                print(f"Request {i+1}: Success - {len(result)} assets")
            else:
                print(f"Request {i+1}: Error - {result['error']}")

asyncio.run(rate_limiting_example())
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig
import json

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )

@app.get("/api/assets")
async def get_assets():
    async with ImmichTools(app.state.config) as tools:
        result = json.loads(await tools.get_all_assets())
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

@app.get("/api/assets/{asset_id}")
async def get_asset(asset_id: str):
    async with ImmichTools(app.state.config) as tools:
        result = json.loads(await tools.get_asset_info(asset_id))
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
```

### CLI Tool

```python
#!/usr/bin/env python3
import asyncio
import argparse
import json
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

async def main():
    parser = argparse.ArgumentParser(description="Immich MCP CLI")
    parser.add_argument("--list-assets", action="store_true")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--asset-id", type=str, help="Get asset info")
    
    args = parser.parse_args()
    
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        if args.list_assets:
            assets = json.loads(await tools.get_all_assets())
            print(json.dumps(assets, indent=2))
        
        if args.search:
            results = json.loads(await tools.search_photos(args.search))
            print(json.dumps(results, indent=2))
        
        if args.asset_id:
            info = json.loads(await tools.get_asset_info(args.asset_id))
            print(json.dumps(info, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

## Environment-Specific Examples

### Development Environment

```bash
# .env.development
IMMICH_BASE_URL=http://localhost:2283/api
IMMICH_API_KEY=dev-key
IMMICH_TIMEOUT=60
```

### Production Environment

```bash
# .env.production
IMMICH_BASE_URL=https://immich.yourdomain.com/api
IMMICH_API_KEY=production-key
IMMICH_TIMEOUT=30
```

### Docker Environment

```bash
# docker-compose.yml
version: '3.8'
services:
  immich-mcp:
    image: immich-mcp:latest
    environment:
      - IMMICH_BASE_URL=https://immich.yourdomain.com/api
      - IMMICH_API_KEY=${IMMICH_API_KEY}
    ports:
      - "8000:8000"
```

## Troubleshooting Examples

### Debug Mode

```python
import logging
import asyncio
from immich_mcp.tools import ImmichTools
from immich_mcp.config import ImmichConfig

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def debug_example():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    async with ImmichTools(config) as tools:
        # This will show detailed logs
        result = await tools.get_all_assets()
        print(result)

asyncio.run(debug_example())
```

### Connection Testing

```python
import asyncio
from immich_mcp.config import ImmichConfig

async def test_all_endpoints():
    config = ImmichConfig(
        immich_base_url="https://your-immich-server.com/api",
        immich_api_key="your-api-key"
    )
    
    # Test connection
    if await config.test_connection():
        print("✅ Server connection successful")
    else:
        print("❌ Server connection failed")
        return
    
    # Test API key
    try:
        from immich_mcp.client import ImmichClient
        client = ImmichClient(config)
        assets = await client.get_all_assets()
        print(f"✅ API key valid - found {len(assets)} assets")
    except Exception as e:
        print(f"❌ API key invalid: {e}")

asyncio.run(test_all_endpoints())
```

