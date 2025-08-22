import pytest
import httpx
import respx
from immich_mcp.config import ImmichConfig
from immich_mcp.tools import ImmichTools
import sys

print(sys.path)


@pytest.fixture
def immich_config():
    return ImmichConfig(
        immich_base_url="http://immich.test/api",
        immich_api_key="test-key-is-now-long-enough",
        auth_token="test-auth-token",
    )


@pytest.mark.asyncio
async def test_get_asset_info(immich_config: ImmichConfig):
    asset_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"asset/{asset_id}").mock(
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
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/metadata").mock(
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
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/smart").mock(
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
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/person", params={"name": "test"}).mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_people(name="test")

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_search_places(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/places", params={"name": "test"}).mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_places(name="test")

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_search_suggestions(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("search/suggestions", params={"type": "city"}).mock(
            return_value=httpx.Response(200, json=["test"])
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_search_suggestions(type="city")

        import json

        response = json.loads(result)
        assert response[0] == "test"


@pytest.mark.asyncio
async def test_search_random(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("search/random").mock(
            return_value=httpx.Response(
                200, json=[{"id": "1", "originalFileName": "test.jpg"}]
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_random(size=1)

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_all_people(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("people").mock(
            return_value=httpx.Response(
                200, json={"people": [{"id": "1", "name": "test"}]}
            )
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_people()

        import json

        response = json.loads(result)
        assert response["people"][0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_all_albums(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("albums").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "albumName": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_albums()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_album(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("albums").mock(
            return_value=httpx.Response(201, json={"id": "1", "albumName": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_album(album_name="test")

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_delete_user_license(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete("users/me/license").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_user_license()

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_sign_up_admin(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/admin-sign-up").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.sign_up_admin(user_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_change_password(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/change-password").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.change_password(password_data={"password": "new"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_login(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/login").mock(
            return_value=httpx.Response(201, json={"accessToken": "token"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.login(login_data={"username": "test"})

        import json

        response = json.loads(result)
        assert response["accessToken"] == "token"


@pytest.mark.asyncio
async def test_logout(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/logout").mock(
            return_value=httpx.Response(200, json={"successful": True})
        )

        tools = ImmichTools(immich_config)

        result = await tools.logout()

        import json

        response = json.loads(result)
        assert response["successful"] is True


@pytest.mark.asyncio
async def test_reset_pin_code(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete("auth/pin-code").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.reset_pin_code(pin_code_data={"pinCode": "1234"})

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_setup_pin_code(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/pin-code").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.setup_pin_code(pin_code_data={"pinCode": "1234"})

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_change_pin_code(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("auth/pin-code").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.change_pin_code(pin_code_data={"pinCode": "1234"})

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_lock_auth_session(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/session/lock").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.lock_auth_session()

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_unlock_auth_session(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/session/unlock").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.unlock_auth_session(unlock_data={"password": "test"})

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_get_auth_status(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("auth/status").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_auth_status()

        import json

        response = json.loads(result)
        assert response["status"] == "ok"


@pytest.mark.asyncio
async def test_validate_access_token(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("auth/validateToken").mock(
            return_value=httpx.Response(200, json={"authStatus": True})
        )

        tools = ImmichTools(immich_config)

        result = await tools.validate_access_token()

        import json

        response = json.loads(result)
        assert response["authStatus"] is True


@pytest.mark.asyncio
async def test_get_faces(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("faces", params={"assetId": "1"}).mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_faces(asset_id="1")

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_face(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("faces").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_face(face_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_delete_face(immich_config: ImmichConfig):
    face_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"faces/{face_id}").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_face(face_id=face_id)

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_reassign_faces_by_id(immich_config: ImmichConfig):
    face_id = "1"
    person_id = "2"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"faces/{face_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "personId": "2"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.reassign_faces_by_id(face_id=face_id, person_id=person_id)

        import json

        response = json.loads(result)
        assert response["personId"] == "2"


@pytest.mark.asyncio
async def test_create_person(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("people").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_person(person_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_update_people(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("people").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "updated"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_people(people_data={"name": "updated"})

        import json

        response = json.loads(result)
        assert response[0]["name"] == "updated"


@pytest.mark.asyncio
async def test_delete_people(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete("people").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_people(people_data={"ids": ["1"]})

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_update_person(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"people/{person_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_person(
            person_id=person_id, person_data={"name": "updated"}
        )

        import json

        response = json.loads(result)
        assert response["name"] == "updated"


@pytest.mark.asyncio
async def test_delete_person(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"people/{person_id}").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_person(person_id=person_id)

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_merge_person(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post(f"people/{person_id}/merge").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.merge_person(
            person_id=person_id, merge_data={"ids": ["2"]}
        )

        import json

        response = json.loads(result)
        assert response[0]["success"] is True


@pytest.mark.asyncio
async def test_discover_tools(immich_config: ImmichConfig):
    tools = ImmichTools(immich_config)

    # Test a query that should match multiple categories
    query = "search photo people"
    result = await tools.discover_tools(query)
    import json

    data = json.loads(result)

    # Check that we have some relevant tools
    assert "relevant_tools" in data
    assert len(data["relevant_tools"]) > 0

    # Check for specific tools
    tool_names = [tool["name"] for tool in data["relevant_tools"]]
    assert "search_smart" in tool_names
    assert "search_people" in tool_names
    assert "get_asset_info" in tool_names

    # Test a query that should match only one category
    query = "manage album"
    result = await tools.discover_tools(query)
    data = json.loads(result)
    tool_names = [tool["name"] for tool in data["relevant_tools"]]
    assert "create_album" in tool_names
    assert "delete_album" in tool_names
    assert "search_smart" not in tool_names

    # Test a query that should not match any tools
    query = "what is the weather like"
    result = await tools.discover_tools(query)
    data = json.loads(result)
    assert len(data["relevant_tools"]) == 0


@pytest.mark.asyncio
async def test_reassign_faces(immich_config: ImmichConfig):
    person_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"people/{person_id}/reassign").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "personId": "1"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.reassign_faces(
            person_id=person_id, reassign_data={"faceId": "1"}
        )

        import json

        response = json.loads(result)
        assert response[0]["personId"] == "1"


@pytest.mark.asyncio
async def test_get_all_shared_links(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("shared-links").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_shared_links()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_shared_link(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("shared-links").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_shared_link(link_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_my_shared_link(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("shared-links/me").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_my_shared_link()

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_shared_link_by_id(immich_config: ImmichConfig):
    link_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"shared-links/{link_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_shared_link_by_id(link_id=link_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_remove_shared_link(immich_config: ImmichConfig):
    link_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"shared-links/{link_id}").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.remove_shared_link(link_id=link_id)

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_update_shared_link(immich_config: ImmichConfig):
    link_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.patch(f"shared-links/{link_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_shared_link(
            link_id=link_id, link_data={"name": "updated"}
        )

        import json

        response = json.loads(result)
        assert response["name"] == "updated"


@pytest.mark.asyncio
async def test_remove_shared_link_assets(immich_config: ImmichConfig):
    link_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"shared-links/{link_id}/assets").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.remove_shared_link_assets(link_id=link_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True


@pytest.mark.asyncio
async def test_add_shared_link_assets(immich_config: ImmichConfig):
    link_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"shared-links/{link_id}/assets").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.add_shared_link_assets(link_id=link_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True


@pytest.mark.asyncio
async def test_get_user_license(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("users/me/license").mock(
            return_value=httpx.Response(200, json={"licenseKey": "key"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user_license()

        import json

        response = json.loads(result)
        assert response["licenseKey"] == "key"


@pytest.mark.asyncio
async def test_set_user_license(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("users/me/license").mock(
            return_value=httpx.Response(200, json={"licenseKey": "key"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.set_user_license(license_key="key")

        import json

        response = json.loads(result)
        assert response["licenseKey"] == "key"


@pytest.mark.asyncio
async def test_delete_user_onboarding(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete("users/me/onboarding").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_user_onboarding()

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_get_user_onboarding(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("users/me/onboarding").mock(
            return_value=httpx.Response(200, json={"isOnboarded": True})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user_onboarding()

        import json

        response = json.loads(result)
        assert response["isOnboarded"] is True


@pytest.mark.asyncio
async def test_set_user_onboarding(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("users/me/onboarding").mock(
            return_value=httpx.Response(200, json={"isOnboarded": True})
        )

        tools = ImmichTools(immich_config)

        result = await tools.set_user_onboarding(onboarding_data={"isOnboarded": True})

        import json

        response = json.loads(result)
        assert response["isOnboarded"] is True


@pytest.mark.asyncio
async def test_get_my_preferences(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("users/me/preferences").mock(
            return_value=httpx.Response(200, json={"theme": "dark"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_my_preferences()

        import json

        response = json.loads(result)
        assert response["theme"] == "dark"


@pytest.mark.asyncio
async def test_update_my_preferences(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("users/me/preferences").mock(
            return_value=httpx.Response(200, json={"theme": "light"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_my_preferences(preferences_data={"theme": "light"})

        import json

        response = json.loads(result)
        assert response["theme"] == "light"


@pytest.mark.asyncio
async def test_delete_profile_image(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete("users/profile-image").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_profile_image()

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_create_profile_image(immich_config: ImmichConfig):
    with open("test.jpg", "w") as f:
        f.write("test")

    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("users/profile-image").mock(
            return_value=httpx.Response(201, json={"userId": "1"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_profile_image(file_path="test.jpg")

        import json

        response = json.loads(result)
        assert response["userId"] == "1"


@pytest.mark.asyncio
async def test_get_profile_image(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"users/{user_id}/profile-image").mock(
            return_value=httpx.Response(200, content=b"image data")
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_profile_image(user_id=user_id)

        import base64

        assert result == base64.b64encode(b"image data").decode("utf-8")


@pytest.mark.asyncio
async def test_get_api_keys(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("api-keys").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_api_keys()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_api_key(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("api-keys").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_api_key(key_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_api_key(immich_config: ImmichConfig):
    key_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"api-keys/{key_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_api_key(key_id=key_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_update_api_key(immich_config: ImmichConfig):
    key_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"api-keys/{key_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_api_key(key_id=key_id, key_data={"name": "updated"})

        import json

        response = json.loads(result)
        assert response["name"] == "updated"


@pytest.mark.asyncio
async def test_delete_api_key(immich_config: ImmichConfig):
    key_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"api-keys/{key_id}").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_api_key(key_id=key_id)

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_get_album_info(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"albums/{album_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "albumName": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_album_info(album_id=album_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_all_jobs_status(immich_config: ImmichConfig):
    async with respx.mock:
        respx.get(f"{immich_config.immich_base_url}/api/jobs").mock(
            return_value=httpx.Response(200, json={"job1": "running"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_all_jobs_status()

        import json

        assert json.loads(result) == {"job1": "running"}


@pytest.mark.asyncio
async def test_send_job_command(immich_config: ImmichConfig):
    job_id = "job1"
    command = "start"
    async with respx.mock:
        respx.put(f"{immich_config.immich_base_url}/api/jobs/{job_id}").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.send_job_command(job_id=job_id, command=command)

        import json

        assert json.loads(result) == {"status": "ok"}


@pytest.mark.asyncio
async def test_run_asset_jobs(immich_config: ImmichConfig):
    name = "regenerate-thumbnail"
    asset_ids = ["1", "2"]
    async with respx.mock:
        respx.post(f"{immich_config.immich_base_url}/api/assets/jobs").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.run_asset_jobs(name=name, asset_ids=asset_ids)

        import json

        assert json.loads(result) == {"status": "success"}


@pytest.mark.asyncio
async def test_add_assets_to_album(immich_config: ImmichConfig):
    album_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"albums/{album_id}/assets").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.add_assets_to_album(album_id=album_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True


@pytest.mark.asyncio
async def test_search_users_admin(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("admin/users").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_users_admin()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_user_admin(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("admin/users").mock(
            return_value=httpx.Response(201, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_user_admin(user_data={"name": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_user_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"admin/users/{user_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user_admin(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_update_user_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"admin/users/{user_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_user_admin(
            user_id=user_id, user_data={"name": "updated"}
        )

        import json

        response = json.loads(result)
        assert response["name"] == "updated"


@pytest.mark.asyncio
async def test_delete_user_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"admin/users/{user_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "deleted_user"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.delete_user_admin(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"
        assert response["name"] == "deleted_user"


@pytest.mark.asyncio
async def test_get_user_preferences_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"admin/users/{user_id}/preferences").mock(
            return_value=httpx.Response(200, json={"theme": "dark"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user_preferences_admin(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["theme"] == "dark"


@pytest.mark.asyncio
async def test_update_user_preferences_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"admin/users/{user_id}/preferences").mock(
            return_value=httpx.Response(200, json={"theme": "light"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_user_preferences_admin(
            user_id=user_id, preferences_data={"theme": "light"}
        )

        import json

        response = json.loads(result)
        assert response["theme"] == "light"


@pytest.mark.asyncio
async def test_restore_user_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post(f"admin/users/{user_id}/restore").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.restore_user_admin(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_user_statistics_admin(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"admin/users/{user_id}/statistics").mock(
            return_value=httpx.Response(200, json={"photos": 10})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user_statistics_admin(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["photos"] == 10


@pytest.mark.asyncio
async def test_search_users(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("users").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "name": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_users()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_get_my_user(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("users/me").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_my_user()

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_update_my_user(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put("users/me").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_my_user(user_data={"name": "updated"})

        import json

        response = json.loads(result)
        assert response["name"] == "updated"


@pytest.mark.asyncio
async def test_get_user(immich_config: ImmichConfig):
    user_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"users/{user_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "name": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_user(user_id=user_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_search_memories(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("memories").mock(
            return_value=httpx.Response(200, json=[{"id": "1", "title": "test"}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.search_memories()

        import json

        response = json.loads(result)
        assert response[0]["id"] == "1"


@pytest.mark.asyncio
async def test_create_memory(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.post("memories").mock(
            return_value=httpx.Response(201, json={"id": "1", "title": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.create_memory(memory_data={"title": "test"})

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_get_memory_statistics(immich_config: ImmichConfig):
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get("memories/statistics").mock(
            return_value=httpx.Response(200, json={"total": 1})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_memory_statistics()

        import json

        response = json.loads(result)
        assert response["total"] == 1


@pytest.mark.asyncio
async def test_get_memory(immich_config: ImmichConfig):
    memory_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.get(f"memories/{memory_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "title": "test"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.get_memory(memory_id=memory_id)

        import json

        response = json.loads(result)
        assert response["id"] == "1"


@pytest.mark.asyncio
async def test_update_memory(immich_config: ImmichConfig):
    memory_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"memories/{memory_id}").mock(
            return_value=httpx.Response(200, json={"id": "1", "title": "updated"})
        )

        tools = ImmichTools(immich_config)

        result = await tools.update_memory(
            memory_id=memory_id, memory_data={"title": "updated"}
        )

        import json

        response = json.loads(result)
        assert response["title"] == "updated"


@pytest.mark.asyncio
async def test_delete_memory(immich_config: ImmichConfig):
    memory_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"memories/{memory_id}").mock(return_value=httpx.Response(204))

        tools = ImmichTools(immich_config)

        result = await tools.delete_memory(memory_id=memory_id)

        import json

        response = json.loads(result)
        assert response["status"] == "success"


@pytest.mark.asyncio
async def test_add_memory_assets(immich_config: ImmichConfig):
    memory_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.put(f"memories/{memory_id}/assets").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.add_memory_assets(memory_id=memory_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True


@pytest.mark.asyncio
async def test_remove_memory_assets(immich_config: ImmichConfig):
    memory_id = "1"
    async with respx.mock(base_url=str(immich_config.immich_base_url)) as mock:
        mock.delete(f"memories/{memory_id}/assets").mock(
            return_value=httpx.Response(200, json=[{"success": True}])
        )

        tools = ImmichTools(immich_config)

        result = await tools.remove_memory_assets(memory_id=memory_id, asset_ids=["1"])

        import json

        response = json.loads(result)
        assert response[0]["success"] is True
