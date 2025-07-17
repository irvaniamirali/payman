import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from httpx import Response, TimeoutException, HTTPStatusError, Request, RequestError
from payman.http.api import API, APIError, InvalidJSONResponseError


@pytest.mark.asyncio
async def test_perform_request_returns_json():
    api = API(base_url="https://example.com")
    mock_client = AsyncMock()
    api._client = mock_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"success":true}'
    mock_response.json.return_value = {"success": True}

    mock_client.request = AsyncMock(return_value=mock_response)

    result = await api._perform_request("GET", "/endpoint")
    assert result == {"success": True}
    mock_client.request.assert_awaited_once()


@pytest.mark.asyncio
async def test_perform_request_invalid_json():
    api = API(base_url="https://example.com")
    mock_client = AsyncMock()
    api._client = mock_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "not json"
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

    mock_client.request = AsyncMock(return_value=mock_response)

    with pytest.raises(InvalidJSONResponseError):
        await api._perform_request("GET", "/endpoint")


@pytest.mark.asyncio
async def test_perform_request_http_errors():
    api = API(base_url="https://example.com")
    mock_client = AsyncMock()
    api._client = mock_client

    exc = TimeoutException("timeout")
    mock_client.request = AsyncMock(side_effect=exc)
    with pytest.raises(APIError) as e:
        await api._perform_request("GET", "/endpoint")
    assert e.value.status_code == 408

    request_obj = Request("GET", "https://example.com/endpoint")
    response_obj = Response(status_code=500, request=request_obj, content=b"error")
    exc2 = HTTPStatusError(
        message="HTTP error",
        request=request_obj,
        response=response_obj,
    )
    mock_client.request = AsyncMock(side_effect=exc2)
    with pytest.raises(APIError) as e:
        await api._perform_request("GET", "/endpoint")
    assert e.value.status_code == 500

    exc3 = RequestError("req error")
    mock_client.request = AsyncMock(side_effect=exc3)
    with pytest.raises(APIError) as e:
        await api._perform_request("GET", "/endpoint")
    assert e.value.status_code == 0
