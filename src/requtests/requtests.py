from itertools import cycle
from json import dumps as to_json
import logging
from requests.adapters import BaseAdapter
from requests.models import Response

logger = logging.getLogger(__name__)


class FakeAdapter(BaseAdapter):
    def __init__(self, *responses, assertions=None):
        super().__init__()
        self.responses = _to_generator(responses)
        self.assertions = _to_generator(assertions) if assertions else None

    def close(self):
        pass

    def send(self, request, **kwargs):
        if self.assertions:
            next(self.assertions)(request, **kwargs)
        return next(self.responses)


def fake_request_with_response(**response_config):
    """
    Creates a request function that returns a response given the response_config.
    """
    return fake_request(fake_response(**response_config))


def fake_request(*responses):
    """
    Creates a request function that returns the supplied responses, one at a time.
    Making a new request after the last response has been returned results in a StopIteration error.
    """
    iterator = (response for response in responses)

    def request(method, url, **kwargs):
        return next(iterator)

    return request


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


def _is_iterable(obj):
    return hasattr(obj, "__iter__")


def _to_generator(element_or_collection):
    if _is_iterable(element_or_collection):
        return (x for x in element_or_collection)
    else:
        return cycle([element_or_collection])
