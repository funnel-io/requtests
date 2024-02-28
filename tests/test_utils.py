from json import dumps as to_json
from requests.models import PreparedRequest, Response


def assert_prepared_request(url=None, body=None):
    def assertions(request, **kwargs):
        assert request.url == url
        assert request.body == body

    return assertions


def assert_response(
    response,
    json=None,
    reason=None,
    status_code=200,
    text=None,
    url=None,
    headers={},
):
    assert isinstance(response, Response)
    assert response.status_code == status_code
    assert response.reason == reason
    assert response.url == url
    assert response.headers == headers
    if json is not None:
        assert response._content == to_json(json).encode()
        assert response.json() == json
    if text is not None:
        assert response._content == text.encode()
        assert response.text == text


def build_request(url=None, body=None):
    request = PreparedRequest()
    request.url = url
    request.body = body
    return request
