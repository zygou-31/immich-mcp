import pytest
import httpx
import respx

@pytest.mark.asyncio
async def test_simple():
    async with respx.mock:
        respx.get("https://example.com/").mock(return_value=httpx.Response(200))
        async with httpx.AsyncClient() as client:
            response = await client.get("https://example.com/")
        assert response.status_code == 200
