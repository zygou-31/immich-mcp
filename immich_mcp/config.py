
import os
from pydantic import BaseModel, Field, HttpUrl, SecretStr
from typing import Optional
import httpx

import os
from pydantic import BaseModel, HttpUrl, SecretStr
from typing import Optional
import httpx


class ImmichConfig(BaseModel):
    base_url: HttpUrl
    api_key: SecretStr
    timeout: int = 30
    max_retries: int = 3

    async def test_connection(self) -> bool:
        """Tests the connection to the Immich server."""
        try:
            async with httpx.AsyncClient(base_url=str(self.base_url), headers={"x-api-key": self.api_key.get_secret_value()}) as client:
                response = await client.get("api/server-info/ping")
                response.raise_for_status()
                return True
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Error connecting to Immich: {e}")
            return False
