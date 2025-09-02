class ImmichAPI:
    """A fake client for interacting with the Immich API."""

    def __init__(self, api_url: str | None = None, api_key: str | None = None):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def close(self):
        pass

    async def ping_server(self) -> bool:
        return True

    async def get_my_user(self) -> dict:
        return {
            "id": "test-user-id",
            "email": "test@example.com",
            "name": "Test User",
        }

    async def get_users_list(self) -> list[dict]:
        return [
            {"id": "user1", "email": "user1@example.com", "name": "User One"},
            {"id": "user2", "email": "user2@example.com", "name": "User Two"},
        ]

    async def get_partners(self) -> list[dict]:
        return [
            {
                "id": "partner1",
                "email": "partner1@example.com",
                "name": "Partner One",
                "inTimeline": True,
            },
            {
                "id": "partner2",
                "email": "partner2@example.com",
                "name": "Partner Two",
                "inTimeline": False,
            },
        ]

    async def get_asset(self, asset_id: str) -> dict:
        return {
            "id": asset_id,
            "originalFileName": "test.jpg",
            "type": "IMAGE",
        }

    async def get_my_api_key(self) -> dict:
        return {
            "id": "api-key-1",
            "name": "My API Key",
        }

    async def get_api_key_list(self) -> list[dict]:
        return [
            {"id": "api-key-1", "name": "API Key 1"},
            {"id": "api-key-2", "name": "API Key 2"},
        ]

    async def get_api_key(self, api_key_id: str) -> dict:
        return {
            "id": api_key_id,
            "name": "API Key 1",
        }
