import pytest
import httpx
import respx
from immich_mcp.config import ImmichConfig
from immich_mcp.client import ImmichClient

@pytest.fixture
def immich_config():
    return ImmichConfig(
        immich_base_url="http://immich.test/api",
        immich_api_key="test-key-is-now-long-enough"
    )

@pytest.mark.asyncio
async def test_get_all_assets_success(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "originalFileName": "test.jpg"}])
        )
        
        client = ImmichClient(immich_config)
        assets = await client.get_all_assets()
        
        assert len(assets) == 1
        assert assets[0]["id"] == "1"
        assert assets[0]["originalFileName"] == "test.jpg"

@pytest.mark.asyncio
async def test_get_all_assets_error(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets").mock(
            return_value=httpx.Response(500)
        )
        
        client = ImmichClient(immich_config)
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_all_assets()

@pytest.mark.asyncio
async def test_get_asset_success(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets/{asset_id}").mock(
            return_value=httpx.Response(200, json={"id": asset_id, "originalFileName": "test.jpg"})
        )
        
        client = ImmichClient(immich_config)
        asset = await client.get_asset(asset_id)
        
        assert asset["id"] == asset_id
        assert asset["originalFileName"] == "test.jpg"

@pytest.mark.asyncio
async def test_get_asset_error(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets/{asset_id}").mock(
            return_value=httpx.Response(404)
        )
        
        client = ImmichClient(immich_config)
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_asset(asset_id)

