from requtests.fake_response import fake_response


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
