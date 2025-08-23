# 🧪 Testing

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
