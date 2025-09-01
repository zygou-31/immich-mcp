from unittest.mock import patch

import pytest
from httpx import AsyncClient
from starlette.responses import JSONResponse


# A dummy class to patch
class MyClass:
    def __init__(self):
        pass


# A dummy ASGI app
async def app(scope, receive, send):
    response = JSONResponse({"hello": "world"})
    await response(scope, receive, send)


@pytest.mark.asyncio
async def test_httpx_with_patch():
    with patch("tests.temp_test_httpx.MyClass.__init__", return_value=None):
        async with AsyncClient(app=app, base_url="http://test") as aclient:
            response = await aclient.get("/")
            assert response.status_code == 200
            assert response.json() == {"hello": "world"}
