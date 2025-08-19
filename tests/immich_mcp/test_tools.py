import pytest
import httpx
import respx
from immich_mcp.config import ImmichConfig
from immich_mcp.tools import ImmichTools


@pytest.fixture
def immich_config():
    return ImmichConfig(
        immich_base_url="http://immich.test",
        immich_api_key="test-key-is-now-long-enough",
        auth_token="test-auth-token",
    )


@pytest.mark.asyncio
async def test_get_asset_info(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock:
        respx.get(f"http://immich.test/api/assets/{asset_id}").mock(
            return_value=httpx.Response(
                200, json={"id": asset_id, "originalFileName": "test.jpg"}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_asset_info(asset_id=asset_id)

        import json

        assert json.loads(result) == {"id": asset_id, "originalFileName": "test.jpg"}


@pytest.mark.asyncio
async def test_search_metadata(immich_config: ImmichConfig):
    async with respx.mock:
        respx.post("http://immich.test/api/search/metadata").mock(
            return_value=httpx.Response(
                200,
                json={
                    "assets": {"items": [{"id": "1", "originalFileName": "test.jpg"}]}
                },
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_metadata(description="test")

        import json

        response = json.loads(result)
        assert response["assets"]["items"][0]["id"] == "1"


@pytest.mark.asyncio
async def test_search_smart(immich_config: ImmichConfig):
    async with respx.mock:
        respx.post("http://immich.test/api/search/smart").mock(
            return_value=httpx.Response(
                200,
                json={
                    "assets": {"items": [{"id": "1", "originalFileName": "test.jpg"}]}
                },
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_smart(query="test")

        import json

        response = json.loads(result)
        assert response["assets"]["items"][0]["id"] == "1"


@pytest.mark.asyncio
async def test_search_people(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get("http://immich.test/api/search/person", params={"name": "test"}).mock(
            return_value=httpx.Response(
                200,
                json=[{"id": "1", "name": "test"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_people(name="test")

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_search_places(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get("http://immich.test/api/search/places", params={"name": "test"}).mock(
            return_value=httpx.Response(
                200,
                json=[{"id": "1", "name": "test"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_places(name="test")

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_search_suggestions(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get("http://immich.test/api/search/suggestions", params={"type": "city"}).mock(
            return_value=httpx.Response(
                200,
                json=["test"]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_search_suggestions(type="city")

        import json

        response = json.loads(result)
        assert response[0] == "test"


@pytest.mark.asyncio
async def test_search_random(immich_config: ImmichConfig):
    async with respx.mock:
        respx.post("http://immich.test/api/search/random").mock(
            return_value=httpx.Response(
                200,
                json=[{"id": "1", "originalFileName": "test.jpg"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_random(size=1)

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_all_people(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get("http://immich.test/api/people").mock(
            return_value=httpx.Response(
                200,
                json={"people": [{"id": "1", "name": "test"}]}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_people()

        import json

        response = json.loads(result)
        assert response["people"][0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_all_albums(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get("http://immich.test/api/albums").mock(
            return_value=httpx.Response(
                200,
                json=[{"id": "1", "albumName": "test"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_albums()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_album(immich_config: ImmichConfig):
    async with respx.mock:
        respx.post("http://immich.test/api/albums").mock(
            return_value=httpx.Response(
                201,
                json={"id": "1", "albumName": "test"}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_album(album_name="test")

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_album_info(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock:
        respx.get(f"http://immich.test/api/albums/{album_id}").mock(
            return_value=httpx.Response(
                200,
                json={"id": "1", "albumName": "test"}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_album_info(album_id=album_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_add_assets_to_album(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock:
        respx.put(f"http://immich.test/api/albums/{album_id}/assets").mock(
            return_value=httpx.Response(
                200,
                json=[{"success": True}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.add_assets_to_album(album_id=album_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True
