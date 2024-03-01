import pytest
from requests.models import PreparedRequest
from requtests import ParsedRequest


@pytest.fixture
def prepared_request():
    prepared_request = PreparedRequest()
    prepared_request.prepare(
        method="GET",
        url="https://api.example.com",
        params={"a": 1, "b": 2, "c": [3, 4, 5]},
        json={"some": "data"},
        headers={"Authorization": "Bearer test-token"},
    )
    return prepared_request


def test_parsing_a_prepared_request(prepared_request):
    parsed = ParsedRequest(prepared_request)
    assert isinstance(parsed, ParsedRequest)

    assert parsed.prepared_request is prepared_request
    assert parsed.prepared_request.method == "GET"
    assert parsed.prepared_request.url == "https://api.example.com/?a=1&b=2&c=3&c=4&c=5"
    assert parsed.prepared_request.body == b'{"some": "data"}'
    assert parsed.prepared_request.headers == {
        "Authorization": "Bearer test-token",
        "Content-Length": "16",
        "Content-Type": "application/json",
    }

    assert parsed.method == "GET"
    assert parsed.url == "https://api.example.com/"
    assert parsed.url_params == {"a": "1", "b": "2", "c": ["3", "4", "5"]}
    assert parsed.headers == {
        "Authorization": "Bearer test-token",
        "Content-Length": "16",
        "Content-Type": "application/json",
    }
    assert parsed.json == {"some": "data"}
