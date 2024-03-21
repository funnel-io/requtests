from json import JSONDecodeError
import pytest
import re
from requtests import ParsedRequest
from requtests.parsed_request import CannotParseBodyAsJSON
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


@pytest.fixture
def parsed_request(prepared_request):
    return ParsedRequest(prepared_request)


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
    assert parsed.query == {"a": "1", "b": "2", "c": ["3", "4", "5"]}
    assert parsed.json == {"some": "data"}
    assert parsed.text == '{"some": "data"}'


def test_json_with_an_empty_body(parsed_request):
    parsed_request.prepared_request.body = None
    expected_message = "the JSON object must be str, bytes or bytearray, not NoneType"
    with pytest.raises(CannotParseBodyAsJSON, match=expected_message) as exc_info:
        parsed_request.json
    underlying_error = exc_info.value.error
    assert isinstance(underlying_error, TypeError)


def test_json_with_an_invalid_json_body(parsed_request):
    parsed_request.prepared_request.body = '{"broken": "json'
    expected_message = re.escape("Unterminated string starting at: line 1 column 12 (char 11)")
    with pytest.raises(CannotParseBodyAsJSON, match=expected_message) as exc_info:
        parsed_request.json
    underlying_error = exc_info.value.error
    assert isinstance(underlying_error, JSONDecodeError)


def test_text_with_an_empty_body(parsed_request):
    parsed_request.prepared_request.body = None
    assert parsed_request.text == ""


def test_repr(parsed_request):
    assert repr(parsed_request) == "<ParsedRequest [GET]>"
