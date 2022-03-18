import logging
from json import dumps as to_json
from requests.models import Response

logger = logging.getLogger(__name__)


def fake_response(
    data=None,
    json=None,
    reason=None,
    status_code=200,
    text=None,
    url=None,
    headers={},
):
    """
    Returns a populated instance of Response.
    """
    if data is not None:
        logger.warning("The keyword 'data' is deprecated in favour of using 'json'.")
        json = data

    response = Response()
    response._content = _content(json, text)
    response.reason = reason
    response.status_code = status_code
    response.url = url
    response.headers = headers
    return response


def _content(json, text):
    if json is not None:
        return to_json(json).encode()
    elif text is not None:
        return text.encode()
