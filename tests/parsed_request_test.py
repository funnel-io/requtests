from requests.models import PreparedRequest
from requtests import ParsedRequest


def test_parsing_a_prepared_request():
    prepared_request = PreparedRequest()
    parsed_request = ParsedRequest(prepared_request)
    assert isinstance(parsed_request, ParsedRequest)
    assert parsed_request.prepared_request is prepared_request
