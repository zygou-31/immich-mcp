import pytest
import httpx
import respx
from immich_mcp.config import ImmichConfig
from immich_mcp.client import ImmichClient


@pytest.fixture
def immich_config():
    return ImmichConfig(
        immich_base_url="http://immich.test/api",
        immich_api_key="test-key-is-now-long-enough",
        auth_token="test_auth_token",
    )


@pytest.mark.asyncio
async def test_get_asset_success(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"asset/{asset_id}").mock(
            return_value=httpx.Response(
                200, json={"id": asset_id, "originalFileName": "test.jpg"}
            )
        )

        client = ImmichClient(immich_config)
        asset = await client.get_asset(asset_id)

        assert asset["id"] == asset_id
        assert asset["originalFileName"] == "test.jpg"


@pytest.mark.asyncio
async def test_get_asset_error(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"asset/{asset_id}").mock(return_value=httpx.Response(404))

        client = ImmichClient(immich_config)
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_asset(asset_id)


@pytest.mark.asyncio
async def test_get_all_people_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("people").mock(
            return_value=httpx.Response(
                200,
                json={
                    "people": [
                        {
                            "id": "1",
                            "name": "John Doe",
                            "thumbnailPath": "/path/to/thumb.jpg",
                        }
                    ],
                    "total": 1,
                },
            )
        )

        client = ImmichClient(immich_config)
        people = await client.get_all_people()

        assert len(people["people"]) == 1
        assert people["people"][0]["name"] == "John Doe"
        assert people["total"] == 1


@pytest.mark.asyncio
async def test_get_person_success(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"people/{person_id}").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": person_id,
                    "name": "John Doe",
                    "thumbnailPath": "/path/to/thumb.jpg",
                    "faces": [],
                },
            )
        )

        client = ImmichClient(immich_config)
        person = await client.get_person(person_id)

        assert person["id"] == person_id
        assert person["name"] == "John Doe"


@pytest.mark.asyncio
async def test_get_person_error(immich_config: ImmichConfig):
    person_id = "999"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"people/{person_id}").mock(return_value=httpx.Response(404))

        client = ImmichClient(immich_config)
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_person(person_id)


@pytest.mark.asyncio
async def test_get_person_statistics_success(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"people/{person_id}/statistics").mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalAssets": 10,
                    "totalSize": 1024000,
                    "oldestDate": "2020-01-01",
                    "newestDate": "2023-12-31",
                },
            )
        )

        client = ImmichClient(immich_config)
        stats = await client.get_person_statistics(person_id)

        assert stats["totalAssets"] == 10
        assert stats["totalSize"] == 1024000


@pytest.mark.asyncio
async def test_get_person_thumbnail_success(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"people/{person_id}/thumbnail").mock(
            return_value=httpx.Response(200, content=b"fake_thumbnail_data")
        )

        client = ImmichClient(immich_config)
        thumbnail = await client.get_person_thumbnail(person_id)

        assert thumbnail == b"fake_thumbnail_data"


@pytest.mark.asyncio
async def test_search_metadata_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/metadata").mock(
            return_value=httpx.Response(200, json={"assets": {"items": [{"id": "1"}]}})
        )

        client = ImmichClient(immich_config)
        results = await client.search_metadata({"q": "test"})

        assert "assets" in results
        assert len(results["assets"]["items"]) == 1


@pytest.mark.asyncio
async def test_search_smart_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/smart").mock(
            return_value=httpx.Response(200, json=[{"id": "1"}])
        )

        client = ImmichClient(immich_config)
        results = await client.search_smart({"q": "test"})

        assert len(results) == 1


@pytest.mark.asyncio
async def test_search_people_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/person").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        client = ImmichClient(immich_config)
        results = await client.search_people("test")

        assert len(results) == 1


@pytest.mark.asyncio
async def test_search_places_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/places").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        client = ImmichClient(immich_config)
        results = await client.search_places("test")

        assert len(results) == 1


@pytest.mark.asyncio
async def test_get_search_suggestions_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/suggestions").mock(
            return_value=httpx.Response(200, json=["test"])
        )

        client = ImmichClient(immich_config)
        results = await client.get_search_suggestions("test")

        assert len(results) == 1


@pytest.mark.asyncio
async def test_search_random_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/random").mock(
            return_value=httpx.Response(200, json=[{"id": "1"}])
        )

        client = ImmichClient(immich_config)
        results = await client.search_random({})

        assert len(results) == 1


@pytest.mark.asyncio
async def test_get_all_albums_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("albums").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "albumName": "test"}])
        )

        client = ImmichClient(immich_config)
        albums = await client.get_all_albums()

        assert len(albums) == 1


@pytest.mark.asyncio
async def test_create_album_success(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("albums").mock(
            return_value=httpx.Response(201, json={"id": "1", "albumName": "test"})
        )

        client = ImmichClient(immich_config)
        album = await client.create_album("test")

        assert album["albumName"] == "test"


@pytest.mark.asyncio
async def test_get_album_info_success(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"albums/{album_id}").mock(
            return_value=httpx.Response(200, json={"id": album_id, "albumName": "test"})
        )

        client = ImmichClient(immich_config)
        album = await client.get_album(album_id)

        assert album["id"] == album_id


@pytest.mark.asyncio
async def test_delete_album_success(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"albums/{album_id}").mock(return_value=httpx.Response(204))

        client = ImmichClient(immich_config)
        await client.delete_album(album_id)


@pytest.mark.asyncio
async def test_add_assets_to_album_success(immich_config: ImmichConfig):
    album_id = "1"
    asset_ids = ["1", "2"]
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"albums/{album_id}/assets").mock(
            return_value=httpx.Response(
                200, json=[{"success": True, "id": "1"}, {"success": True, "id": "2"}]
            )
        )

        client = ImmichClient(immich_config)
        results = await client.add_assets_to_album(album_id, asset_ids)

        assert len(results) == 2


@pytest.mark.asyncio
async def test_remove_assets_from_album_success(immich_config: ImmichConfig):
    album_id = "1"
    asset_ids = ["1", "2"]
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"albums/{album_id}/assets").mock(
            return_value=httpx.Response(
                200, json=[{"success": True, "id": "1"}, {"success": True, "id": "2"}]
            )
        )

        client = ImmichClient(immich_config)
        results = await client.remove_assets_from_album(album_id, asset_ids)

        assert len(results) == 2
