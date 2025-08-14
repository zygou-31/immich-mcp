import pytest
import httpx
import respx
from immich_mcp.config import ImmichConfig
from immich_mcp.tools import ImmichTools


@pytest.fixture
def immich_config():
    return ImmichConfig(
        immich_base_url="http://immich.test/api",
        immich_api_key="test-key-is-now-long-enough",
    )


@pytest.mark.asyncio
async def test_get_asset_info(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets/{asset_id}").mock(
            return_value=httpx.Response(
                200, json={"id": asset_id, "originalFileName": "test.jpg"}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_asset_info(asset_id=asset_id)

        import json

        assert json.loads(result) == {"id": asset_id, "originalFileName": "test.jpg"}


@pytest.mark.asyncio
async def test_get_all_assets(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets").mock(
            return_value=httpx.Response(
                200, json=[{"id": "1", "originalFileName": "test.jpg"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_assets()

        import json

        assets = json.loads(result)
        assert len(assets) == 1
        assert assets[0]["id"] == "1"
        assert assets[0]["originalFileName"] == "test.jpg"


@pytest.mark.asyncio
async def test_get_asset_info_error(immich_config: ImmichConfig):
    asset_id = "999"
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets/{asset_id}").mock(
            return_value=httpx.Response(404, json={"error": "Asset not found"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_asset_info(asset_id=asset_id)

        import json

        response = json.loads(result)
        assert "error" in response


@pytest.mark.asyncio
async def test_get_all_assets_error(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/assets").mock(
            return_value=httpx.Response(500, json={"error": "Server error"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_assets()

        import json

        response = json.loads(result)
        assert "error" in response
