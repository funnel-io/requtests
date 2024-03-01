from requests.models import PreparedRequest
from requtests import parse_request, ParsedRequest


def test_parse_request():
    prepared_request = PreparedRequest
    parsed_request = parse_request(prepared_request)
    assert isinstance(parsed_request, ParsedRequest)
    assert parsed_request.prepared_request is prepared_request
