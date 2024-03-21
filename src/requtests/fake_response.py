from json import dumps as to_json
from requests.models import Response
from requests.structures import CaseInsensitiveDict


def fake_response(
    json=None,
    reason=None,
    status_code=200,
    text=None,
    url=None,
    headers=None,
) -> Response:
    """
    Returns a populated instance of requests.models.Response.
    """

    response = Response()
    response._content = _content(json, text)
    response.reason = reason
    response.status_code = status_code
    response.url = url
    response.headers = CaseInsensitiveDict(**(headers or {}))
    return response


def _content(json, text):
    if json is not None:
        return to_json(json).encode()
    elif text is not None:
        return text.encode()
