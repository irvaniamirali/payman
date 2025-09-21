import pytest
import respx
from httpx import Response

from payman.core.http.client import AsyncHttpClient
from payman.core.exceptions.http import (
    HttpStatusError, InvalidJsonError
)


@pytest.mark.asyncio
@respx.mock
async def test_successful_request():
    respx.post("http://test/api").mock(
        return_value=Response(200, json={"ok": True})
    )

    async with AsyncHttpClient(base_url="http://test") as client:
        resp = await client.request("POST", "/api", json_data={"a": 1})
        assert resp == {"ok": True}


@pytest.mark.asyncio
@respx.mock
async def test_http_status_error():
    respx.get("http://test/fail").mock(
        return_value=Response(400, text="Bad Request")
    )

    async with AsyncHttpClient(base_url="http://test") as client:
        with pytest.raises(HttpStatusError) as exc_info:
            await client.request("GET", "/fail")

        assert exc_info.value.status_code == 400
        assert "Bad Request" in exc_info.value.body


@pytest.mark.asyncio
@respx.mock
async def test_invalid_json_response():
    respx.get("http://test/notjson").mock(
        return_value=Response(200, text="Not JSON")
    )

    async with AsyncHttpClient(base_url="http://test") as client:
        with pytest.raises(InvalidJsonError):
            await client.request("GET", "/notjson")
