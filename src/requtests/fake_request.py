from functools import partial
from requtests.fake_response import fake_response


def fake_delete(*responses):
    return partial(fake_request(*responses), "delete")


def fake_get(*responses):
    return partial(fake_request(*responses), "get")


def fake_head(*responses):
    return partial(fake_request(*responses), "head")


def fake_options(*responses):
    return partial(fake_request(*responses), "options")


def fake_patch(*responses):
    return partial(fake_request(*responses), "patch")


def fake_post(*responses):
    return partial(fake_request(*responses), "post")


def fake_put(*responses):
    return partial(fake_request(*responses), "put")


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
