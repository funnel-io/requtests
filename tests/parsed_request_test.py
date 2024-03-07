import pytest
from requtests import ParsedRequest
from tests.test_utils import build_request


@pytest.fixture
def prepared_request():
    return build_request(
        method="GET",
        url="https://api.example.com",
        params={"a": 1, "b": 2, "c": [3, 4, 5]},
        json={"some": "data"},
        headers={"Authorization": "Bearer test-token"},
    )


def test_parsing_a_prepared_request(prepared_request):
    assert prepared_request is prepared_request
    assert prepared_request.method == "GET"
    assert prepared_request.url == "https://api.example.com/?a=1&b=2&c=3&c=4&c=5"
    assert prepared_request.body == b'{"some": "data"}'
    assert prepared_request.headers == {
        "Authorization": "Bearer test-token",
        "Content-Length": "16",
        "Content-Type": "application/json",
    }

    parsed = ParsedRequest(prepared_request)
    assert isinstance(parsed, ParsedRequest)

    assert parsed.prepared_request is prepared_request
    assert parsed.method is prepared_request.method
    assert parsed.url is prepared_request.url
    assert parsed.body is prepared_request.body
    assert parsed.headers is prepared_request.headers

    assert parsed.endpoint == "https://api.example.com/"
    assert parsed.url_params == {"a": "1", "b": "2", "c": ["3", "4", "5"]}
    assert parsed.json == {"some": "data"}
    assert parsed.text == '{"some": "data"}'


@pytest.mark.skip
def test_endpoint():
    pass


@pytest.mark.skip
def test_url_params():
    pass


@pytest.mark.skip
def test_json_with_an_empty_body():
    pass


@pytest.mark.skip
def test_json_with_an_invalid_json_body():
    pass


@pytest.mark.skip
def test_text_with_an_empty_body():
    pass
