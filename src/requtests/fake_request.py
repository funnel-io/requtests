from functools import partial
from requests import Session
from .fake_adapter import FakeAdapter
from .fake_response import fake_response
from .protocols import OptionalAssertions, Responder


def fake_delete(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "delete")


def fake_get(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "get")


def fake_head(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "head")


def fake_options(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "options")


def fake_patch(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "patch")


def fake_post(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "post")


def fake_put(*responses, assertions: OptionalAssertions = None) -> Responder:
    return partial(fake_request(*responses, assertions=assertions), "put")


def fake_request_with_response(
    assertions: OptionalAssertions = None,
    **response_config,
) -> Responder:
    """
    Creates a request function that returns a response given the response_config.
    """
    return fake_request(fake_response(**response_config), assertions=assertions)


def fake_request(*responses, assertions: OptionalAssertions = None) -> Responder:
    """
    Creates a request function that returns the supplied responses, one at a time.
    Making a new request after the last response has been returned results in a StopIteration error.
    """
    adapter = FakeAdapter(*responses, assertions=assertions)
    session = Session()
    setattr(session, "get_adapter", lambda url: adapter)
    return session.request
