from payman.core.exceptions.http import HttpStatusError


def test_http_status_error_properties():
    exc = HttpStatusError(500, "boom", body="fail")
    assert exc.status_code == 500
    assert exc.body == "fail"
    assert "boom" in str(exc)
