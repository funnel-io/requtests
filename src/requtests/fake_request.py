from functools import partial
from requests import Session
from requtests.fake_adapter import FakeAdapter
from requtests.fake_response import fake_response


def fake_delete(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "delete")


def fake_get(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "get")


def fake_head(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "head")


def fake_options(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "options")


def fake_patch(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "patch")


def fake_post(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "post")


def fake_put(*responses, assertions=None):
    return partial(fake_request(*responses, assertions=assertions), "put")


def fake_request_with_response(assertions=None, **response_config):
    """
    Creates a request function that returns a response given the response_config.
    """
    return fake_request(fake_response(**response_config), assertions=assertions)


def fake_request(*responses, assertions=None):
    """
    Creates a request function that returns the supplied responses, one at a time.
    Making a new request after the last response has been returned results in a StopIteration error.
    """
    adapter = FakeAdapter(*responses, assertions=assertions)
    session = Session()
    session.get_adapter = lambda url: adapter
    return session.request
