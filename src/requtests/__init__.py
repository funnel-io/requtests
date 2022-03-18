from .fake_adapter import FakeAdapter
from .fake_request import fake_request, fake_request_with_response
from .fake_response import fake_response

VERSION = "1.0.0"

__all__ = [
    FakeAdapter,
    fake_request,
    fake_request_with_response,
    fake_response,
]
